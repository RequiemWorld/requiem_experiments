## Discovery #1 - Ansible discourages using the root user directly

- Issue Encountered: Running the ansible playbook command against a host that could be SSH'd into manually resulted in a permission error. This was due to it trying to sign in as a non-root user to sudo to root from there.
- Identified Solution (might require more than this in production, like disabling password based ssh logins completely): add the -u option to the ansible-playbook command to login as root, e.g, ``ansible-playbook -i xxx.xxx.xxx.xxx, 00-static-playbook-nginx.yaml -u root`` 
- Potential Future Solution: Before anything using ansible, setup an additional user and install the SSH key with the cloud-init config, so that ansible can use it to sudo to root instead.
    - Part of the above solution might also be a solution to not being able to have the same public key on an account under multiple names.

## Discovery #2 - Ansible doesn't have an option to override the SSH port?
- Issue Encountered: When designing something to automate ansible, I was unable to find an option to pass to the ansible-playbook utility for specifying the SSH port. 

## Discovery #3 - Ansible won't use private keys that are publicly readable/open will make files that way.
- Issue Encountered: A temporary directory was created and the private key file was written to a file in it. When the file path to the private key was given to ansible, it refused to use it because it had 0644 permissions, where it was publicly accessible to every user. [\[1\]](https://ibb.co/23Z1KfL5)
- Security Notice: The temporary directory should have 700 permissions, only accessible to the user running python. The file created in the directory by default will have 644 permissions, making it publicly accessible. The directory it is in is not publicly accessible so it can't be accessed by path. If the file is moved elsewhere it may pose a security risk. Ansible will refuse to use it. [\[1\]](https://heitorpb.github.io/bla/pytmp/)
- Security/Solution: Before the contents are written, we can harden the permissions of the file, to add actual security and get ansible to use it. 