"""
A better interface over digitalocean's pydo package. Created specifically for the project and what we use.
"""
import pydo
import enum
from enum import StrEnum
from ._ssh import DigitalOceanSSHKeyManager
from ._ssh import SSHKeyCreationInfo

# It is possible that at runtime in the future, it can be verified that these
# are still valid and fail the script early if they're not, valid ones can be found at: https://slugs.do-api.dev/
class ImageSlug(enum.StrEnum):
	UBUNTU_24_04_X64 = "ubuntu-24-04-x64"
	ROCKY_LINUX_8_x64 = "rockylinux-8-x64"

class RegionSlug(enum.StrEnum):
	NYC1 = "NYC1"

class SizeSlug(enum.StrEnum):
	S_1VCPU_512MB_10GB = "s-1vcpu-512mb-10gb"
	S_1VCPU_1GB = "s-1vcpu-1gb"
	S_2VCPU_2GB_90GB_INTEL = "s-2vcpu-2gb-90gb-intel"

class DropletStatus(StrEnum):
	NEW = "new"
	ACTIVE = "active"

class DropletSSHKeyEntry:
	def __init__(self, id_or_fingerprint: int | str):
		self._id_or_fingerprint = id_or_fingerprint

	@property
	def id_or_fingerprint(self):
		return self._id_or_fingerprint

class DropletCreationRequest:

	def __init__(self,
				 name: str,
				 region: RegionSlug | str,
				 size: SizeSlug | str,
				 image: ImageSlug | str,
				 user_data: str | None = None,
				 ssh_keys: list[int | str] = None):
		"""
		:param name: The name to give to the droplet (may also be the hostname)
		:param region: The region that the droplet should be hosted in (e.g., NYC1)
		:param size: The size of the droplet in the digital ocean the machine will be (e.g., s-2vcpu-4gb-amd).
		:param image: The operating system image to use for the droplet (e.g., ubuntu-24-04-x64)
		:param user_data: The script or cloud-init config to use to initialize the server with.
		:param ssh_keys: A list of identifiers or fingerprints for the public keys to install for the root user of the machine.
		"""
		self._name = name
		self._region = region
		self._size = size
		self._image = image
		self._user_data = user_data
		self._ssh_keys = ssh_keys.copy() if ssh_keys is not None else []

	def to_dictionary_for_api(self) -> dict:
		request_dictionary = {
			"name": self._name,
			"region": self._region,
			"size": self._size,
			"image": self._image,
			"user_data": self._user_data,
			"ssh_keys": self._ssh_keys.copy()}
		return request_dictionary

	@property
	def name(self) -> str:
		return self._name

	@property
	def region(self) -> str:
		return self._region

	@property
	def size(self) -> str:
		return self._size

	@property
	def image(self) -> str:
		return self._image


class DropletNetworkType(StrEnum):
	PUBLIC = "public"
	PRIVATE = "private"

class IPv4Network:
	def __init__(self, ip_address: str, type: DropletNetworkType):
		self._ip_address = ip_address
		self._type = type

	@property
	def ip_address(self):
		return self._ip_address


class DropletNetworkInfo:
	def __init__(self, ipv4_networks: list[IPv4Network]):
		self._ipv4_networks = ipv4_networks.copy()

	@property
	def ipv4(self) -> list[IPv4Network]:
		return self._ipv4_networks.copy()


class DropletCreationResult:
	def __init__(self, id: int, status: str):
		self._id = id
		self._status = status

	@classmethod
	def from_api_response_dictionary(cls, response_data: dict):
		droplet = response_data["droplet"]
		return DropletCreationResult(droplet["id"], droplet["status"])

	@property
	def id(self):
		"""
		The identifier assigned to the droplet by digitalocean.
		"""
		return self._id

	@property
	def status(self) -> str:
		"""
		The status of the container e.g. 'active' like weather ot not it is started.
		"""
		return self._status


class DropletGetResult:
	def __init__(self, id: int, name: str, status: DropletStatus | str,  network_info: DropletNetworkInfo):
		self._id = id
		self._name = name
		self._status = status
		self._network_info = network_info

	@classmethod
	def from_droplet_dictionary(cls, data: dict) -> "DropletGetResult":
		id = data["id"]
		name = data["name"]
		status = data["status"]
		ipv4_networks = []
		for network in data["networks"]["v4"]:
			ipv4_networks.append(IPv4Network(network["ip_address"], network["type"]))
		return cls(id, name, status, DropletNetworkInfo(ipv4_networks))

	@property
	def id(self) -> int:
		"""
		The identifier assigned to the droplet by digitalocean.
		"""
		return self._id

	@property
	def name(self) -> str:
		"""
		The name that was given to the droplet on creation.
		"""
		return self._name

	@property
	def status(self) -> str | DropletStatus:
		return self._status


	@property
	def ipv4_networks(self) -> list[IPv4Network]:
		"""
		Presumably, the network interfaces on the droplet, with weather they're private,
		public, and with their IP address, netmask, and gateway as appropriate, with only IP address to start.
		"""
		return self._network_info.ipv4



class DigitalOceanDropletManager:
	def __init__(self, pydo_client: pydo.Client):
		self._pydo_client = pydo_client

	def create_droplet(self, request: DropletCreationRequest) -> DropletCreationResult:
		raw_droplet_response_dictionary = self._pydo_client.droplets.create(request.to_dictionary_for_api())
		return DropletCreationResult.from_api_response_dictionary(raw_droplet_response_dictionary)

	def get_droplet(self, droplet_id: int) -> DropletGetResult:
		return DropletGetResult.from_droplet_dictionary(self._pydo_client.droplets.get(droplet_id)["droplet"])


class DigitalOceanClient:
	def __init__(self, pydo_client: pydo.Client):
		self._pydo_client = pydo_client
		self._droplet_manager = DigitalOceanDropletManager(pydo_client)
		self._ssh_key_manager = DigitalOceanSSHKeyManager(pydo_client)

	@property
	def droplets(self) -> DigitalOceanDropletManager:
		return self._droplet_manager

	@property
	def ssh_keys(self) -> DigitalOceanSSHKeyManager:
		return self._ssh_key_manager
