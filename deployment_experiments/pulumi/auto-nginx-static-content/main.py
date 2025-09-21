import _import_helper
import os
import click
import pulumi
import pulumi_tls
import pulumi.automation as automation
import pulumi_cloudflare as cloudflare
import pulumi_digitalocean as digitalocean
from pulumi_random import RandomUuid
from pulumi_cloudflare import get_zone
from pulumi_command.remote import CopyToRemote, Command, ConnectionArgs
from pulumi_helper.local import setup_pulumi_workspace_options
from pulumi_helper import drop_into_ssh


def _pulumi_program() -> None:
	config = pulumi.Config()
	static_content_root = config.require("static-content-root")
	root_domain_name = config.require("root-domain-name")

	private_ssh_key = pulumi_tls.PrivateKey("private-key-1", algorithm="RSA", rsa_bits=2048)
	do_ssh_key = digitalocean.SshKey("do-ssh-key", public_key=private_ssh_key.public_key_openssh)
	droplet = digitalocean.Droplet(
		resource_name="static-content-droplet",
		region=digitalocean.Region.NYC1,
		image="ubuntu-24-04-x64",
		size=digitalocean.DropletSlug.DROPLET_S1_VCPU2_GB,
		ssh_keys=[do_ssh_key.id],
		user_data="#!/bin/bash\napt update nginx -y\napt install nginx -y\n"
	)

	random_subdomain_name = RandomUuid("random_subdomain")
	root_domain_zone_id = get_zone({"name": root_domain_name}).zone_id  # has to be .zone_id, not .id
	site_dns_record = cloudflare.DnsRecord(
		"dns_record",
		zone_id=root_domain_zone_id,
		ttl=1, # ' ttl must be set to 1 when `proxied` is true: When a DNS record is marked as `proxied` the TTL must be 1 as Cloudflare will control the TTL internally.'
		type="A",
		name=random_subdomain_name.result,
		content=droplet.ipv4_address,
		proxied=True)
	connection_arguments = ConnectionArgs(
		host=droplet.ipv4_address,
		user="root",
		private_key=private_ssh_key.private_key_openssh)
	make_var_www_html = Command(
		"make-var-www-html",
		opts=pulumi.ResourceOptions(depends_on=[droplet]),
		connection=connection_arguments,
		create="mkdir -p /var/www/html")  # this may or may not avoid a race condition
	CopyToRemote(
		"static-content-upload",
		opts=pulumi.ResourceOptions(depends_on=[make_var_www_html]),
		connection=connection_arguments, source=pulumi.FileArchive(static_content_root), remote_path="/var/www/html/")
	pulumi.export("droplet_ipv4_address", droplet.ipv4_address)
	pulumi.export("static_content_domain", pulumi.Output.concat(site_dns_record.name, ".", root_domain_name))
	pulumi.export("private_ssh_key", private_ssh_key.private_key_openssh)

@click.command()
@click.argument("action")
@click.argument("passphrase", required=True)
@click.option("--static-root")
@click.option("--domain-name")
@click.option("--do-token", envvar=["DIGITAL_OCEAN_TOKEN"], required=True)
@click.option("--cf-token", envvar=["CLOUDFLARE_TOKEN"], required=True)
def main(action: str, passphrase: str, static_root: str | None, domain_name: str | None, do_token: str, cf_token: str) -> None:
	import logging
	logging.basicConfig(level=logging.DEBUG)
	workspace_options = setup_pulumi_workspace_options(
		project_name="project_name",
		backend_directory="./pulumi-backend",
		secret_passphrase=passphrase,
		environment_variables={"DIGITALOCEAN_TOKEN": do_token, "CLOUDFLARE_API_TOKEN": cf_token})
	if action == "up":
		assert static_root is not None, "static root argument required"
		assert os.path.isdir(static_root), "is not a path to a directory"
		stack = automation.create_or_select_stack("experimental", "project_name", program=_pulumi_program, opts=workspace_options)
		stack.set_config("static-content-root", automation.ConfigValue(static_root))
		stack.set_config("root-domain-name", automation.ConfigValue(domain_name))
		up_result = stack.up(debug=True)
		print(up_result.stderr)
		print(up_result.stdout)
		print(f"static content should be deployed to {stack.outputs().get('droplet_ipv4_address')} with domain {stack.outputs().get('static_content_domain')}")
	elif action == "down":
		stack = automation.select_stack("experimental", "project_name", program=_pulumi_program, opts=workspace_options)
		print(f"destroying stack and should be removing droplet with ip {stack.outputs().get('droplet_ipv4_address')} and domain {stack.outputs().get('static_content_domain')}")
		stack.destroy(debug=True)
	elif action == "ssh":
		stack = automation.select_stack("experimental", "project_name", program=_pulumi_program, opts=workspace_options)
		droplet_ip_address = stack.outputs().get("droplet_ipv4_address").value
		private_ssh_key_openssh = stack.outputs().get("private_ssh_key").value
		drop_into_ssh(private_ssh_key_openssh, droplet_ip_address, "root")



if __name__ == '__main__':
	main()