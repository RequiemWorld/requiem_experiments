import os
import click
import pulumi
import pulumi.automation as automation
from pulumi_digitalocean import Region
from pulumi_digitalocean import Droplet
from pulumi.automation import ProjectBackend
from pulumi.automation import ProjectSettings
from pulumi.automation import LocalWorkspaceOptions


def _single_droplet_program() -> None:
	sole_droplet = Droplet(
		resource_name="droplet-name",
		region=Region.NYC1,
		image="ubuntu-24-04-x64",
		size="s-1vcpu-1gb-amd",
		user_data="#!/bin/bash\napt update nginx -y\napt install nginx -y\n")
	pulumi.export("droplet_ipv4_address", sole_droplet.ipv4_address)


def _setup_pulumi_workspace_options(
		project_name: str,
		backend_directory: str,
		secret_passphrase: str,
		digital_ocean_token: str) -> LocalWorkspaceOptions:
	"""
	:param backend_directory: The directory that will contain the .pulumi directory with state, locks, etc.
	:param secret_passphrase: The password used to encrypt any secrets (this uses a local backend so they're probably stored/encrypted there).
	"""
	work_directory_absolute_path = os.path.abspath(backend_directory)
	project_settings = ProjectSettings(
		name=project_name,
		runtime="python",
		backend=ProjectBackend(f"file://{work_directory_absolute_path}"))
	env_vars = {
		"DIGITALOCEAN_TOKEN": digital_ocean_token,
		"PULUMI_CONFIG_PASSPHRASE": secret_passphrase}
	return LocalWorkspaceOptions(project_settings=project_settings, env_vars=env_vars)


@click.command()
@click.argument("action")
@click.argument("secret_passphrase")
# https://unix.stackexchange.com/questions/8223/can-other-users-view-the-arguments-passed-to-a-command
# It would be nice to use click to manage arguments passed via environment variables,
# but to make them available that way they have to have a normal argument available as well.
#
# Having secrets passed by command line argument is not secure since it may be possible
# for any user on the system to see the processes running and what arguments were passed in.
@click.option("--do-token", envvar=["DIGITAL_OCEAN_TOKEN"], required=True)
def main(action: str, secret_passphrase: str, do_token: str) -> None:
	stack_name = "production"
	project_name = "pulumi-minimal"
	backend_directory = "./pulumi-local-backend"
	os.makedirs(backend_directory, exist_ok=True)
	workspace_options = _setup_pulumi_workspace_options(project_name, backend_directory, secret_passphrase, do_token)
	if action == "up":
		stack = automation.create_or_select_stack(stack_name, project_name, program=_single_droplet_program, opts=workspace_options)
		stack.up(debug=True)
		print(f"droplet should be available with ipv4 address: {stack.outputs().get('droplet_ipv4_address')}")
	elif action == "down":
		stack = automation.select_stack(stack_name, project_name, program=_single_droplet_program, opts=workspace_options)
		print(f"should be tearing down droplet with IPv4 address {stack.outputs().get('droplet_ipv4_address')}")
		stack.destroy()


if __name__ == "__main__":
	main()