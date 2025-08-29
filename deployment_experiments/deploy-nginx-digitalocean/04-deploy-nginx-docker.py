import os
import pydo
from paramiko import RSAKey
from betterdo import DigitalOceanClient, DropletCreationRequest, RegionSlug, SizeSlug, ImageSlug
from betterdo.extra import DockerRunCommand, CloudInitConfig
from betterdo.extra import wait_for_droplet_to_come_online
from betterdo.extra import wait_for_tcp4_connectivity
from betterdo.extra import IdempotentSSHKey
from betterssh import SimpleSSHClient

def install_docker_on_ubuntu_machine(ssh_client: SimpleSSHClient) -> None:
	ssh_client.execute_command("apt update -y")
	ssh_client.execute_command("apt install  -y " + " ".join(["apt-transport-https", "ca-certificates", "curl", "software-properties-common"]))
	ssh_client.execute_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
	ssh_client.execute_command('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
	# turns out that apt update is necessary after updating the repositories
	ssh_client.execute_command("apt -o DPkg::Lock::Timeout=5 update -y")
	ssh_client.execute_command("apt install docker-ce -y ")

def create_nginx_docker_container_on_host(ssh_client: SimpleSSHClient, publish_to_port: int) -> None:
	ssh_client.execute_command(f"docker run -d --name nginx -p {publish_to_port}:80 nginx:latest")


def main() -> None:
	client = DigitalOceanClient(pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN")))
	ssh_key = IdempotentSSHKey.from_id_rsa_file_in_ssh_directory("name", "id_rsa.pub")
	ssh_key_info = ssh_key.ensure_existence(client)
	creation_request = DropletCreationRequest(
		name="nginx12345",
		region=RegionSlug.NYC1,
		size=SizeSlug.S_2VCPU_2GB_90GB_INTEL,
		image=ImageSlug.UBUNTU_24_04_X64,
		ssh_keys=[ssh_key_info.id])
	droplet_creation_info = client.droplets.create_droplet(creation_request)
	droplet_get_info = wait_for_droplet_to_come_online(client, droplet_creation_info.id)
	server_ip_address = droplet_get_info.ipv4_networks[0].ip_address
	wait_for_tcp4_connectivity(server_ip_address, 22, try_for_seconds=120)
	default_rsa_key = RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
	with SimpleSSHClient.from_host_and_key(host=server_ip_address, port=22, key=default_rsa_key, username="root") as ssh_client:
		install_docker_on_ubuntu_machine(ssh_client)
		create_nginx_docker_container_on_host(ssh_client, 80)

	print("IP address of host that should be running nginx docker container", droplet_get_info.ipv4_networks[0].ip_address)

if __name__ == "__main__":
	main()