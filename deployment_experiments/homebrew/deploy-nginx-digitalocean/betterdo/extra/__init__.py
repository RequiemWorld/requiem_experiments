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
		# TODO decide on behavior for adding the same package twice
		self._package_names.append(package_name)

	def add_packages(self, package_names: list[str]):
		# TODO decide on behavior for adding the same package twice
		self._package_names.extend(package_names)

	def add_run_command(self, command: str):
		"""
		Add a command to be added to the 'runcmd:' section when config is converted to string of YAML.
		"""
		self._run_commands.append(command)


class DockerRunCommand:
	"""
	Create and run a new container from an image
	~ https://docs.docker.com/reference/cli/docker/container/run/
	"""
	def __init__(self, image_name: str, container_name: str | None = None, publish_ports: dict[int, int] | None = None):
		"""
		:param publish_ports: <port_on_container>:<port_on_host">
		"""
		self._image_name = image_name
		self._container_name = container_name
		self._published_ports: dict[int, int] = publish_ports if publish_ports is not None else {}
		self._environment_variables: dict[str, str] = dict()
		self._name_for_container: str | None = None

	def __str__(self):
		command = ["docker", "run"]
		if self._name_for_container is not None:
			command.extend(["--name", self._name_for_container])
		for container_port, host_port in self._published_ports.items():
			# https://stackoverflow.com/questions/20845056/how-can-i-expose-more-than-1-port-with-docker
			command.extend(["-p", f"{host_port}:{container_port}"])
		command.append(self._image_name)  # image name to create container from comes last
		return " ".join(command)

	def to_string(self):
		"""
		Sort of an alias for __str__, more ergonomic to type when starting by typing out the variable name.
		"""
		return str(self)

	def publish_port(self, container_port: int, host_port: int):
		"""
		Publish a port from the container to the host on the given host port.
		"""
		self._published_ports[container_port] = host_port

	def add_environment_variable(self, name: str, value: str) -> None:
		"""
		An environment variable to set in the container.
		"""
		self._environment_variables[name] = value

	def add_container_name(self, name_for_container: str) -> None:
		"""The name to give to the container that will be created from the image with --name argument."""
		self._name_for_container = name_for_container


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
