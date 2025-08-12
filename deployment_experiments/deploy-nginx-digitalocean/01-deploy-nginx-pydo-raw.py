import os
import pydo
import time

client = pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN"))

user_data = """#cloud-config
package_update: true
package_upgrade: true
packages:
  - nginx

runcmd:
  - systemctl daemon-reload
  - systemctl enable nginx.service
  - systemctl start --no-block nginx.service
"""

# https://slugs.do-api.dev/
droplet = client.droplets.create({
	"name": "nginx-server",
	"region": "nyc1",
	"size": "s-1vcpu-1gb",
	"image": "ubuntu-24-04-x64",
	"user_data": user_data,
})["droplet"]

while True:
	droplet_get_result = client.droplets.get(droplet['id'])["droplet"]
	status = droplet_get_result["status"]
	if status == "active":
		break
	time.sleep(1)

droplet_info = client.droplets.get(droplet['id'])["droplet"]
ip_address = droplet_info['networks']['v4'][0]['ip_address']
print(f"Nginx server deployed at: {ip_address}")
