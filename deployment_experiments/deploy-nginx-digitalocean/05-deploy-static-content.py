import os
import uuid

import cloudflare
import paramiko
import pydo
from paramiko import RSAKey

from betterdo import SizeSlug
from betterdo import DropletGetResult
from betterdo import DropletCreationRequest
from betterdo import DigitalOceanClient, RegionSlug, ImageSlug
from betterdo.extra import IdempotentSSHKey
from betterdo.extra import wait_for_tcp4_connectivity
from betterdo.extra import wait_for_droplet_to_come_online
from betterssh import SimpleSSHClient


def wait_for_apt_lock_availability(ssh_client: SimpleSSHClient) -> None:
	# -o DPkg::Lock::Timeout=5 and other amounts of seconds worked previously,
	# it proved to be flaky on further deployments though, so this solution is preferred instead.
	ssh_client.execute_command("while sudo lsof /var/lib/dpkg/lock-frontend; do echo 'Waiting for apt to finish...'; sleep 5; done")


def install_docker_on_ubuntu_machine(ssh_client: SimpleSSHClient) -> None:
	ssh_client.execute_command("apt-get -o DPkg::Lock::Timeout=50 update -y")
	wait_for_apt_lock_availability(ssh_client)
	ssh_client.execute_command("apt-get -o DPkg::Lock::Timeout=50 install  -y " + " ".join(["apt-transport-https", "ca-certificates", "curl", "software-properties-common"]))
	wait_for_apt_lock_availability(ssh_client)
	ssh_client.execute_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
	wait_for_apt_lock_availability(ssh_client)
	ssh_client.execute_command('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
	# turns out that apt update is necessary after updating the repositories
	ssh_client.execute_command("apt-get update -y")
	wait_for_apt_lock_availability(ssh_client)
	ssh_client.execute_command("apt-get  install docker-ce -y ")

def create_nginx_docker_container_on_host(
		ssh_client: SimpleSSHClient,
		publish_to_port: int,
		static_content_host_path: str) -> None:
	ssh_client.execute_command(f"docker run -v {static_content_host_path}:/usr/share/nginx/html:ro -d --name nginx -p {publish_to_port}:80 nginx:latest")

def make_server_and_get_ipv4_address(client: DigitalOceanClient, ssh_key: IdempotentSSHKey) -> str:
	creation_request = DropletCreationRequest(
		name="static-content",
		# region and droplet size hardcoded for simplicity
		region=RegionSlug.NYC1,
		size=SizeSlug.S_2VCPU_2GB_90GB_INTEL,
		image=ImageSlug.UBUNTU_24_04_X64,
		ssh_keys=[ssh_key.ensure_existence(client).id])
	droplet_creation_info = client.droplets.create_droplet(creation_request)
	droplet_get_info = wait_for_droplet_to_come_online(client, droplet_creation_info.id)
	server_ip_address = droplet_get_info.ipv4_networks[0].ip_address
	return server_ip_address

def make_server_with_nginx_and_static_content(
		client: DigitalOceanClient, static_content_root: str) -> str:
	
	"""
	Returns the IP address of the server
	"""
	ssh_key = IdempotentSSHKey.from_id_rsa_file_in_ssh_directory("name", "id_rsa.pub")
	server_ip_address = make_server_and_get_ipv4_address(client, ssh_key)
	wait_for_tcp4_connectivity(server_ip_address, 22, try_for_seconds=120)

	default_rsa_key = RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
	with SimpleSSHClient.from_host_and_key(server_ip_address, 22, default_rsa_key, "root") as ssh_client:
		ssh_client.enable_debug_mode()
		ssh_client.files.upload_directory(static_content_root, "/opt/static_content")
		install_docker_on_ubuntu_machine(ssh_client)
		create_nginx_docker_container_on_host(ssh_client, publish_to_port=80, static_content_host_path="/opt/static_content")
	return server_ip_address

def find_zone_id_for_domain_name(client: cloudflare.Cloudflare, domain_name: str) -> str:
	zones = client.zones.list()
	for zone in zones:
		if zone.name == domain_name:
			return zone.id
	raise ValueError(f"No zone found for domain {domain_name}")


def main() -> None:
	# This script isn't really meant to be clean, so much as work out specifics for the idea.
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--static-content-root",
						help="the directory with static content to serve as the root of the webserver.", required=True)

	parser.add_argument("--base-domain-on-cloudflare", help="e.g, example.com", required=True)
	arguments = parser.parse_args()
	static_content_root = arguments.static_content_root
	do_client = DigitalOceanClient(pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN")))
	cf_client = cloudflare.Cloudflare(api_token=os.getenv("CLOUDFLARE_TOKEN"))
	assert os.path.exists(static_content_root), f"static content path {static_content_root} does not exist"
	assert os.path.isdir(static_content_root), f"static content path {static_content_root} is not a directory"

	server_ip_address = make_server_with_nginx_and_static_content(do_client, static_content_root)
	zone_id = find_zone_id_for_domain_name(cf_client, arguments.base_domain_on_cloudflare)
	random_domain_name = f"{uuid.uuid4()}.{arguments.base_domain_on_cloudflare}"
	# proxied MUST be set to True or else by default it will just be the original domain, probably should add a smoke test for this.
	cf_client.dns.records.create(zone_id=zone_id, type="A", name=random_domain_name, content=server_ip_address, proxied=True)
	print(f"Created DNS record for {random_domain_name} pointing to {server_ip_address}")

if __name__ == "__main__":
	main()