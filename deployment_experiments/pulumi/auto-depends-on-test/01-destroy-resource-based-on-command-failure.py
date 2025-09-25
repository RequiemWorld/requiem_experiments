import _import_helper
import click
import pulumi
from pulumi import ResourceOptions
from pulumi_command.local import Command
from pulumi_random import RandomUuid
from pulumi_helper import ExploratoryPulumiExecutor


def _pulumi_program():
	config = pulumi.config.Config()
	should_fail_deployment = config.require("should_fail_deployment").lower() in ["yes", "y", "true"]
	if should_fail_deployment:
		command_string = "exit 1"
	else:
		command_string = "exit 0"
	# this arbitrary resource won't be destroyed when the creation of a dependent resource fails
	arbitrary_resource = RandomUuid("random_uuid")
	arbitrary_fail_or_pass_command = Command(
		resource_name="command_name",
		opts=ResourceOptions(depends_on=arbitrary_resource),
		create=command_string)


@click.command()
@click.argument("action")
@click.argument("fail_deployment")
def main(action: str, fail_deployment: str) -> None:
	from pulumi.automation import ConfigValue
	executor = ExploratoryPulumiExecutor(project_name="requiem", backend_directory="./local-smoke", secret_passphrase="whatever", environment={})
	if action == "up":
		executor.up_and_print("stack", _pulumi_program, {"should_fail_deployment": ConfigValue(fail_deployment)})
	elif action == "down":
		executor.destroy_and_print("stack", _pulumi_program)

if __name__ == '__main__':
	main()