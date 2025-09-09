import io
import shutil
import tempfile
import subprocess
from pathlib import Path
from paramiko import RSAKey


# https://stackoverflow.com/questions/32297456/how-to-ignore-ansible-ssh-authenticity-checking
def _make_and_run_ansible_playbook_command(ssh_host: str, playbook_path: str, private_key_path: str, as_user: str) -> None:
	"""
	:raises RuntimeError: When there is an error in running the ansible command
	"""
	command = [
		shutil.which("ansible-playbook"),
		"-i", f"{ssh_host},",
		"-u", as_user,
		"--private-key", private_key_path,
		playbook_path]
	environment = {"ANSIBLE_HOST_KEY_CHECKING": "false"}
	try:
		subprocess.check_call(command, env=environment)
	except subprocess.CalledProcessError as e:
		breakpoint()
		raise RuntimeError from e


class SimplePlaybookExecutor:
	def __init__(self, ssh_host: str, rsa_private_key: RSAKey) -> None:
		"""
		:param ssh_host: The address or hostname of the SSH server. The SSH port must be 22.
		"""
		self._ssh_host = ssh_host
		self._rsa_private_key = rsa_private_key

	def _get_private_key_as_string(self) -> str:
		string_buffer = io.StringIO()
		self._rsa_private_key.write_private_key(string_buffer)
		return string_buffer.getvalue()

	def execute(self, playbook_path: str, as_user: str = "root"):
		"""
		Executes ansible playbook against the configured ssh host.
		"""
		with tempfile.TemporaryDirectory() as temp_directory:
			rsa_private_key_file_path = Path(temp_directory).joinpath("is_rsa")
			rsa_private_key_file_path.touch(0o600)
			rsa_private_key_file_path.write_text(self._get_private_key_as_string())
			_make_and_run_ansible_playbook_command(
				ssh_host=self._ssh_host,
				playbook_path=playbook_path,
				private_key_path=str(rsa_private_key_file_path),
				as_user=as_user)