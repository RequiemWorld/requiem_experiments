import pydo
from pydo.exceptions import HttpResponseError


class SSHKeyCreationInfo:
	def __init__(self, name: str, public_key: str):
		"""
		:param name: A human-readable name for the key when putting it on the account.
		:param public_key: The entire public key string that will be embedded into the root user's authorized_keys file. (e.g., ssh-rsa ...)
		"""
		self._name = name
		self._public_key = public_key

	def to_dictionary_for_api(self) -> dict:
		return {"name": self._name, "public_key": self._public_key}

	@property
	def name(self):
		return self._name

	@property
	def public_key(self):
		return self._public_key


class SSHKeyCreationResult:

	def __init__(self, id: int, name: str, public_key: str, fingerprint: str):
		self._id = id
		self._name = name
		self._public_key = public_key
		self._fingerprint = fingerprint

	@property
	def id(self) -> int:
		return self._id

	@property
	def name(self) -> str:
		return self._name

	@property
	def public_key(self) -> str:
		return self._public_key

	@property
	def fingerprint(self) -> str:
		return self._fingerprint

	@staticmethod
	def from_ssh_key_dictionary(response_dictionary: dict) -> "SSHKeyCreationResult":
		return SSHKeyCreationResult(
			id=response_dictionary["id"],
			name=response_dictionary["name"],
			public_key=response_dictionary["public_key"],
			fingerprint=response_dictionary["fingerprint"])


class SSHKeyInformation:
	def __init__(self, id: int, name: str, public_key: str, fingerprint: str):
		self._id = id
		self._name = name
		self._public_key = public_key
		self._fingerprint = fingerprint

	@property
	def id(self) -> int:
		return self._id

	@property
	def name(self) -> str:
		return self._name

	@property
	def public_key(self) -> str:
		return self._public_key

	@property
	def fingerprint(self) -> str:
		return self._fingerprint

	@staticmethod
	def from_ssh_key_dictionary(response_dictionary: dict) -> "SSHKeyInformation":
		return SSHKeyInformation(
			id=response_dictionary["id"],
			name=response_dictionary["name"],
			public_key=response_dictionary["public_key"],
			fingerprint=response_dictionary["fingerprint"])


class DigitalOceanSSHKeyManager:
	def __init__(self, client: pydo.Client):
		self._client = client

	def create_key(self, info: SSHKeyCreationInfo) -> SSHKeyInformation:
		"""
		:raises HttpResponseError: When there is an error while trying to create the SSH Key on the account.
		"""

		key_creation_info = info.to_dictionary_for_api()
		ssh_key_dictionary = self._client.ssh_keys.create(key_creation_info)["ssh_key"]
		return SSHKeyInformation.from_ssh_key_dictionary(ssh_key_dictionary)

	def delete_key(self, id_or_fingerprint: int | str) -> None:
		"""
		:param id_or_fingerprint: The numeric identifier (e.g., 512189) or the fingerprint of the key (e.g., "3b:16:bf:e4:8b:00:8b:b8:59:8c:a9:d3:f0:19:45:fa")
		:raises HttpResponseError: When there is an error while trying to delete the SSH Key from the account.
		"""
		# It's a path parameter, as stated in:
		# https://docs.digitalocean.com/reference/api/digitalocean/#tag/SSH-Keys/operation/sshKeys_delete
		self._client.ssh_keys.delete(ssh_key_identifier=id_or_fingerprint)

	def list_keys(self) -> list[SSHKeyInformation]:
		# FIXME The results will be paginated, not sure how I want to handle this yet.
		"""
		:raises HttpResponseError: When there is an error while trying to list the SSH Keys on the account.
		"""
		ssh_keys = self._client.ssh_keys.list()["ssh_keys"]
		return [SSHKeyInformation.from_ssh_key_dictionary(key) for key in ssh_keys]
