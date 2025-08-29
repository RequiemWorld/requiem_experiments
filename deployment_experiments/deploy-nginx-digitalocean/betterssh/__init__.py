import os
import paramiko
from paramiko.rsakey import RSAKey
from ._path_helper import LocalToRemoteFileWalker



class SimpleSSHFiles:
	def __init__(self, ssh_client: paramiko.SSHClient, debug_mode: bool = False):
		self._ssh_client = ssh_client
		self._debug_mode = debug_mode

	def enable_debug_mode(self):
		self._debug_mode = True

	def upload_directory(self, local_path: str, remote_path: str):
		sftp = self._ssh_client.open_sftp()
		local_to_remote_walker = LocalToRemoteFileWalker(local_path, remote_path)
		try:
			for local_path, remote_path in local_to_remote_walker.walk():
				remote_dir = os.path.dirname(remote_path)
				try:
					sftp.stat(remote_dir)
					if self._debug_mode:
						print(f"Directory already exists: {remote_dir}")
				except FileNotFoundError:
					if self._debug_mode:
						print(f"Creating directory: {remote_dir}")
					sftp.mkdir(remote_dir)

				if self._debug_mode:
					print(f"Uploading file: {local_path} -> {remote_path}")
				sftp.put(local_path, remote_path)
		finally:
			sftp.close()


class SimpleSSHClient:
	"""
	A simple SSH client for connecting to servers and executing commands
	"""
	def __init__(self, ssh_client: paramiko.SSHClient, debug_mode: bool = False):
		self._ssh_client = ssh_client
		self._debug_mode = debug_mode
		self._file_management: SimpleSSHFiles = SimpleSSHFiles(ssh_client)

	@property
	def files(self) -> SimpleSSHFiles:
		return self._file_management

	def enable_debug_mode(self):
		self._debug_mode = True
		self._file_management.enable_debug_mode()

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

