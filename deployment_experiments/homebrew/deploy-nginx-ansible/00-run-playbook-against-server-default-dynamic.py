import os
import sys
from playbook_helper import SimplePlaybookExecutor
from paramiko import RSAKey

# The idea is to go from a loaded paramiko.RSAKey, and a playbook file, to running it against the server.
ssh_rsa_key = RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
ssh_host = sys.argv[1]
playbook_executor = SimplePlaybookExecutor(ssh_host, ssh_rsa_key)
playbook_executor.execute("./00-static-playbook-nginx.yaml", as_user="root")
