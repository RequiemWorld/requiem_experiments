import sys
from typing import Callable
from pulumi import automation as automation
from pulumi.automation import UpResult, ConfigValue
from pulumi.automation import DestroyResult
from .local import setup_pulumi_workspace_options


class ExploratoryPulumiExecutor:
	_PRINT_STDOUT = lambda string: print(string)
	_PRINT_STDERR = lambda string: print(string, file=sys.stderr)

	def __init__(self, project_name: str, backend_directory: str, secret_passphrase: str, environment: dict[str, str]):
		if "PULUMI_CONFIG_PASSPHRASE" in environment:
			raise ValueError
		self._project_name = project_name
		self._backend_directory = backend_directory
		self._secret_passphrase = secret_passphrase
		self._workspace_options = setup_pulumi_workspace_options(
			project_name=project_name,
			backend_directory=backend_directory,
			secret_passphrase=secret_passphrase,
			environment_variables=environment.copy())

	def up_and_print(self, stack_name: str, program: Callable, config: dict[str, ConfigValue] | None = None) -> UpResult:
		stack = automation.create_or_select_stack(
			stack_name=stack_name,
			project_name=self._project_name,
			program=program,
			opts=self._workspace_options)
		if config is None:
			config = {}
		for key, value in config.items():
			stack.set_config(key, value)
		# self.<lambda> is treated as a method on the class where self is passed as the first argument, hence this code.
		return stack.up(on_output=ExploratoryPulumiExecutor._PRINT_STDOUT, on_error=ExploratoryPulumiExecutor._PRINT_STDERR)

	def destroy_and_print(self, stack_name: str, program: Callable) -> DestroyResult:
		stack = automation.select_stack(
			stack_name=stack_name,
			project_name=self._project_name,
			program=program,
			opts=self._workspace_options)
		return stack.destroy(on_error=ExploratoryPulumiExecutor._PRINT_STDERR, on_output=ExploratoryPulumiExecutor._PRINT_STDOUT)
