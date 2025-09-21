import os
import shutil
import tempfile
from pathlib import Path


def drop_into_ssh(private_key_openssh_string: str, droplet_ip_address: str, user: str) -> None:
	"""
	:raises RuntimeError: When the SSH utility can't be found.
	"""
	if shutil.which("ssh") is None:
		raise RuntimeError("ssh utility could not be found")
	with tempfile.TemporaryDirectory() as temp_dir:
		key_file_path = Path(temp_dir) / 'temp_key'
		key_file_path.write_text(private_key_openssh_string)
		key_file_path.chmod(0o600)
		os.system(f'ssh -i {key_file_path} {user}@{droplet_ip_address}')
