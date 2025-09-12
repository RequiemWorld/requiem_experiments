import argparse
import os
import socket
import sys
import tempfile
import subprocess
import time
from pathlib import Path


def wait_for_tcp4_connectivity(host: str, port: int, wait_for_seconds: int):
	"""
	:raises TimeoutError: when unable to connect to <host:port> in time.
	"""
	time_started_waiting = time.time()
	seconds_spent_waiting: int = 0
	while seconds_spent_waiting < wait_for_seconds:
		connect_socket = socket.socket()
		connect_socket.settimeout(1)
		try:
			connect_socket.connect((host, port))
			return
		except (TimeoutError, ConnectionRefusedError):
			seconds_spent_waiting = int(time.time() - time_started_waiting)
		finally:
			connect_socket.close()
	raise TimeoutError("couldn't connect to {host}:{port} in time")


# An idea behind this script is that for using ansible with terraform,
# we'll be installing ansible through python/pip, so having an accompanying script
# which is only tied to the standard library isn't such a burden and is cross-platform.
def main() -> None:
	# The ansible-playbook utility requires the path to a file containing the private key,
	# the private key is more or less (effectively) only in memory in terraform. This script
	# will help with executing playbooks on a single host and take the private key data by environment variable.
	#
	# When we enter the local-exec block in terraform after a server has been created, it won't necessarily
	# be online with SSH available yet, so this script will also wait for connectivity before using ansible-playbook.
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--playbook-path", required=True)
	parser.add_argument("-t", "--target-host", required=True)
	parser.add_argument("-u", "--login-as-user", required=True)
	parser.add_argument("-w", "--wait-for-seconds", default=120, type=int)
	arguments = parser.parse_args()
	playbook_path = arguments.playbook_path
	rsa_key_string = os.environ["RSA_PRIVATE_KEY"]
	assert "OPENSSH PRIVATE KEY" in rsa_key_string
	with tempfile.TemporaryDirectory() as temp_directory:
		temp_rsa_key_path = Path(temp_directory) / "id_rsa"
		temp_rsa_key_path.touch(mode=0o600)
		temp_rsa_key_path.write_text(rsa_key_string)
		print(f"waiting for connectivity to {arguments.target_host}:22")
		try:
			wait_for_tcp4_connectivity(arguments.target_host, 22, arguments.wait_for_seconds)
		except TimeoutError:
			print(f"unable to connect to {arguments.target_host}:22 after trying for {arguments.wait_for_seconds} seconds", file=sys.stderr)
			sys.exit(1)

		playbook_command = [
			"ansible-playbook", "-i", f"{arguments.target_host},",
			"-u", arguments.login_as_user,
			"--private-key", str(temp_rsa_key_path),
			playbook_path]
		subprocess.check_call(playbook_command)

if __name__ == "__main__":
	main()