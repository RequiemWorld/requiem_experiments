import os
import pydo
import time

# This script is relevant because we're not in production at the time of writing this,
# every droplet created is just for testing, and many of them are created back-to-back to save time

# AI generated based on the previous file
client = pydo.Client(os.getenv("DIGITAL_OCEAN_TOKEN"))
droplets = client.droplets.list()["droplets"]
print(f"Found {len(droplets)} droplets")
if input("Are you sure you want to delete EVERY droplet on the account?") != "Yes":
	exit()
for droplet in droplets:
	print(f"Deleting droplet: {droplet['name']} (ID: {droplet['id']})")
	client.droplets.destroy(droplet['id'])
	time.sleep(1)

print("All droplets have been deleted")
