import paramiko
from paramiko.rsakey import RSAKey


class SimpleSSHClient:
	"""
	A simple SSH client for connecting to servers and executing commands
	"""
	def __init__(self, ssh_client: paramiko.SSHClient, debug_mode: bool = False):
		self._ssh_client = ssh_client
		self._debug_mode = debug_mode

	def enable_debug_mode(self):
		self._debug_mode = True

	@classmethod
	def from_host_and_key(cls, host: str, port: int, key: RSAKey, username: str) -> "SimpleSSHClient":
		paramiko_client = paramiko.SSHClient()
		paramiko_client.set_missing_host_key_policy(paramiko.WarningPolicy())
		paramiko_client.connect(host, port, pkey=key, username=username)
		return cls(paramiko_client)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._ssh_client.close()

	@property
	def connect(self):
		return self._ssh_client.connect

	def execute_command(self, command: str) -> int:
		"""
		:returns: the exit code from running the command.
		"""
		stdin, stdout, stderr = self._ssh_client.exec_command(command)
		if self._debug_mode:
			stdout_data = stdout.read().decode('utf-8')
			stderr_data = stderr.read().decode('utf-8')
			print("COMMAND:", command)
			print("STDOUT:", stdout_data)
			print("STDERR:", stderr_data)
		exit_status = stdout.channel.recv_exit_status()
		stdout.channel.close()
		return exit_status

