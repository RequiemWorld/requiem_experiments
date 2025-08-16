import os
import pydo
import time
from betterdo import SizeSlug
from betterdo import RegionSlug
from betterdo import ImageSlug
from betterdo import DigitalOceanClient, DropletStatus
from betterdo import DropletCreationRequest
from betterdo import DropletGetResult
from betterdo.extra import CloudInitConfig
from betterdo.extra import wait_for_droplet_to_come_online


def main() -> None:
	# The same script as before but with a new/better interface over pydo
	client = DigitalOceanClient(pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN")))
	# copying the user data from the last file to this one resulted in formatting issues,
	# so I've taken the liberty of adding a way to build a cloud-init config with code earlier on.
	cloud_init_config = CloudInitConfig()
	cloud_init_config.add_package("nginx")
	cloud_init_config.add_run_command("systemctl daemon reload")
	cloud_init_config.add_run_command("systemctl enable nginx")
	cloud_init_config.add_run_command("systemctl start --no-block nginx")
	creation_request = DropletCreationRequest(
		name="nginx",
		region=RegionSlug.NYC1,
		size=SizeSlug.S_1VCPU_1GB,
		image=ImageSlug.UBUNTU_24_04_X64,
		user_data=cloud_init_config.to_user_data())
	creation_result = client.droplets.create_droplet(creation_request)
	ready_droplet_info = wait_for_droplet_to_come_online(client, creation_result.id)
	print(ready_droplet_info.ipv4_networks[0].ip_address)

if __name__ == '__main__':
	main()