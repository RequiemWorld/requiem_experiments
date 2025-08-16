"""
Extra stuff provided here for now to make working with the cloud more convenient.
"""

class CloudInitConfig:
	def __init__(self):
		self._package_names: list[str] = list()
		self._run_commands: list[str] = list()

	def __str__(self):
		indent = "  "
		yaml_string = ""
		yaml_string += "packages:\n"
		for package_name in self._package_names:
			yaml_string += indent + f"- {package_name}\n"
		yaml_string += "runcmd:\n"
		for command_string in self._package_names:
			yaml_string += indent + f"- {command_string}\n"
		return yaml_string

	def to_user_data(self) -> str:
		return "#cloud-config\n" + str(self)

	def add_package(self, package_name: str):
		"""
		Add a name of a package to be added to the 'package:' section when config is converted to string of YAML.
		"""
		self._package_names.append(package_name)

	def add_run_command(self, command: str):
		"""
		Add a command to be added to the 'runcmd:' section when config is converted to string of YAML.
		"""
		self._run_commands.append(command)
