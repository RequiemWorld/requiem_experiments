import os
from .. import DigitalOceanClient
from .._ssh import SSHKeyInformation, SSHKeyCreationInfo


# This may or may not be idempotency, I don't have a better word for it right now.
class IdempotencyError(Exception):
	pass


class IdempotencyBrokenError(IdempotencyError):
	pass

class IdempotentSSHKey:
	"""
	A class for creating an SSH key on the account idempotently. A local file
	with the public SSH key can be loaded and given a name, and if the one on
	the account with the same name matches, it will succeed, if non-existent, one created.

	If the local and remote information do not match, it should fail
	"""
	def __init__(self, name: str, public_key: str):
		"""
		:param public_key: The public key in ssh-rsa <base64> format.
		:raises AssertionError: When public_key does not start with 'ssh-rsa '.
		"""
		assert public_key.startswith("ssh-rsa ")
		self._name = name
		self._public_key = public_key

	@classmethod
	def from_id_rsa_file_in_ssh_directory(cls, name: str, file_name: str) -> "IdempotentSSHKey":
		"""
		:param name: The name to give to the resource on the digital ocean account.
		:param file_name: The file name in the ~/.ssh directory e.g., id_rsa.pub.
		"""
		ssh_key_path = os.path.expanduser(f"~/.ssh/{file_name}")
		with open(ssh_key_path, "r") as f:
			public_key_data = f.read()
		return IdempotentSSHKey(name, public_key_data)

	@staticmethod
	def _find_key_with_matching_name(client: DigitalOceanClient, name: str) -> SSHKeyInformation | None:
		for key_info in client.ssh_keys.list_keys():
			has_matching_name = key_info.name == name
			if has_matching_name:
				return key_info
		return None

	def ensure_existence(self, client: DigitalOceanClient) -> SSHKeyInformation:
		"""
		:raises HTTPResponseError: When there is an issue listing keys or creating them.
		"""
		key_with_matching_name = self._find_key_with_matching_name(client, self._name)
		if key_with_matching_name is None:
			key_creation_info = SSHKeyCreationInfo(self._name, self._public_key)
			return client.ssh_keys.create_key(key_creation_info)
		else:
			key_has_matching_public_key_value = key_with_matching_name.public_key == self._public_key
			if not key_has_matching_public_key_value:
				raise IdempotencyBrokenError("mismatch between intended public key content and remote key content")
			return key_with_matching_name