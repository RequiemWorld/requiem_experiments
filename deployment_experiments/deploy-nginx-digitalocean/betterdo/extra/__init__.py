"""
Extra stuff provided here for now to make working with the cloud more convenient.
"""
import time
import socket
from .. import DropletStatus
from .. import DropletGetResult
from .. import DigitalOceanClient
from ._ssh import IdempotencyError
from ._ssh import IdempotencyBrokenError
from ._ssh import IdempotentSSHKey

class CloudInitConfig:
	def __init__(self):
		self._package_names: list[str] = list()
		self._run_commands: list[str] = list()

	def __str__(self):
		indent = "  "
		yaml_string = ""
		yaml_string += "packages:\n"
		for package_name in self._package_names:
			yaml_string += indent + f"- {package_name}\n"
		yaml_string += "runcmd:\n"
		for command_string in self._package_names:
			yaml_string += indent + f"- {command_string}\n"
		return yaml_string

	def to_user_data(self) -> str:
		return "#cloud-config\n" + str(self)

	def add_package(self, package_name: str):
		"""
		Add a name of a package to be added to the 'package:' section when config is converted to string of YAML.
		"""
		self._package_names.append(package_name)

	def add_run_command(self, command: str):
		"""
		Add a command to be added to the 'runcmd:' section when config is converted to string of YAML.
		"""
		self._run_commands.append(command)


def wait_for_droplet_to_come_online(client: DigitalOceanClient, droplet_id: int) -> DropletGetResult:
	while True:
		droplet_info = client.droplets.get_droplet(droplet_id)
		if droplet_info.status == DropletStatus.ACTIVE:
			return droplet_info
		time.sleep(0.8)

def wait_for_tcp4_connectivity(host: str, port: int, try_for_seconds: int) -> None:
	time_started_waiting = time.time()
	seconds_elapsed_trying = None
	while seconds_elapsed_trying is None or seconds_elapsed_trying < try_for_seconds:
		with socket.socket() as sock:
			sock.settimeout(1)
			try:
				sock.connect((host, port))
				return
			except (TimeoutError, ConnectionRefusedError):
				pass
		seconds_elapsed_trying = time.time() - time_started_waiting
	raise RuntimeError(f"unable to connect to {host}:{port} in {try_for_seconds} seconds.")
