import os
import pydo
import _import_helper
from paramiko import RSAKey
from betterdo import RegionSlug, DropletCreationRequest
from betterdo import SizeSlug
from betterdo import ImageSlug
from betterdo import DigitalOceanClient
from betterdo.extra import wait_for_droplet_to_come_online, IdempotentSSHKey
from betterdo.extra import wait_for_tcp4_connectivity
from playbook_helper import SimplePlaybookExecutor


def make_new_server_and_wait_for_ssh(client: DigitalOceanClient, public_ssh_key_path: str) -> str:
	"""
	Returns the IP address of the created server
	"""
	idempotent_ssh_key = IdempotentSSHKey.from_id_rsa_file_at_path("name", public_ssh_key_path)
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
	print(f"waiting for connectivity to {droplet_ip_address}:22")
	wait_for_tcp4_connectivity(droplet_ip_address, 22, 120)
	print(f"server should be available at {droplet_ip_address}")
	return droplet_ip_address


def setup_server_with_nginx_via_ansible_playbook(playbook_path: str, ip_address: str, private_key: RSAKey) -> None:
	print(f"configuring server to have installed and started a native version of nginx")
	playbook_executor = SimplePlaybookExecutor(ip_address, private_key)
	playbook_executor.execute(playbook_path, as_user="root")


def main() -> None:
	client = DigitalOceanClient(pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN")))
	ssh_private_key = RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
	server_ip_address = make_new_server_and_wait_for_ssh(client, os.path.expanduser("~/.ssh/id_rsa.pub"))
	setup_server_with_nginx_via_ansible_playbook("00-static-playbook-nginx.yaml", server_ip_address, ssh_private_key)
	wait_for_tcp4_connectivity(server_ip_address, 80, 60)


if __name__ == "__main__":
	main()