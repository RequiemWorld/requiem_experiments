import os
import time
import pydo
import paramiko
from betterdo import ImageSlug
from betterdo import SizeSlug
from betterdo import DropletCreationRequest, DigitalOceanClient
from betterdo import RegionSlug
from paramiko import SSHClient, RSAKey
from betterdo.extra import wait_for_tcp4_connectivity
from betterdo.extra import wait_for_droplet_to_come_online
from betterdo.extra import IdempotentSSHKey


def get_default_ssh_rsa_public_key() -> str:
	default_id_rsa_public_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
	with open(default_id_rsa_public_key_path, "r") as f:
		ssh_rsa_key_string = f.read()
		assert ssh_rsa_key_string.startswith("ssh-rsa ")
	return ssh_rsa_key_string


class ServerPreparationResult:
	def __init__(self, ip_address: str) -> None:
		self._ip_address = ip_address

	@property
	def ip_address(self):
		return self._ip_address


def prepare_arbitrary_ubuntu_server(client: DigitalOceanClient) -> ServerPreparationResult:
	ssh_rsa_public_key_data = get_default_ssh_rsa_public_key()
	idempotent_ssh_key = IdempotentSSHKey(name="name", public_key=ssh_rsa_public_key_data)
	ssh_key_info = idempotent_ssh_key.ensure_existence(client)
	creation_request = DropletCreationRequest(
		name="nginx",
		region=RegionSlug.NYC1,
		size=SizeSlug.S_2VCPU_2GB_90GB_INTEL,
		image=ImageSlug.UBUNTU_24_04_X64,
		ssh_keys=[ssh_key_info.id])
	creation_result = client.droplets.create_droplet(creation_request)
	ready_droplet_info = wait_for_droplet_to_come_online(client, creation_result.id)
	droplet_ip_address = ready_droplet_info.ipv4_networks[0].ip_address
	wait_for_tcp4_connectivity(droplet_ip_address, 22, 120)
	return ServerPreparationResult(droplet_ip_address)


def main() -> None:
	# creates a Ubuntu server, uploads and uses the current default private key under "name"
	# ssh's into the server, installs nginx, and replaced the index.html file with hello world333
	client = DigitalOceanClient(pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN")))
	server_preparation_result = prepare_arbitrary_ubuntu_server(client)
	default_ssh_key = RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
	with SSHClient() as ssh_client:
		ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
		ssh_client.connect(server_preparation_result.ip_address, pkey=default_ssh_key, username="root")
		stdin, stdout, stderr = ssh_client.exec_command("apt update -y")
		# to avoid intermittency since it returns early.
		stdout.channel.recv_exit_status()
		stdin, stdout, stderr = ssh_client.exec_command("apt install nginx -y")
		# to avoid intermittency since it returns early.
		stdout.channel.recv_exit_status()
		stdin, stdout, stderr = ssh_client.exec_command("bash -c 'echo \"hello world333\" > /var/www/html/index.html'")
		# to avoid intermittency since it returns early.
		stdout.channel.recv_exit_status()
	print(f"server should be available with nginx and a hello world page at http://{server_preparation_result.ip_address}")

if __name__ == "__main__":
	main()