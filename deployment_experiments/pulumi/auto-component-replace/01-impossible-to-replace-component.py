import _import_helper
import click
import pulumi
from pulumi import Input
from pulumi.automation import ConfigValue
from pulumi import ResourceOptions
from pulumi_helper import ExploratoryPulumiExecutor


class MyComponent(pulumi.ComponentResource):

	def __init__(self, resource_name: str, input_string: Input[str], opts: pulumi.ResourceOptions = None) -> None:
		super().__init__("requiem:experiments:MyComponent", name=resource_name, props={"input_string": input_string}, opts=opts)


def _pulumi_program() -> None:
	config = pulumi.config.Config()
	input_string = config.require("input_string")
	component = MyComponent("abcd", input_string, opts=ResourceOptions(replace_on_changes=["input_string"]))


@click.command()
@click.argument("action")
@click.argument("input_string")
def main(action: str, input_string: str) -> None:
	executor = ExploratoryPulumiExecutor(project_name="requiem", backend_directory="./local", secret_passphrase="whatever", environment={})
	if action == "up":
		executor.up_and_print("stack", _pulumi_program, {"input_string": ConfigValue(input_string)})
	elif action == "down":
		executor.destroy_and_print("stack", _pulumi_program)


if __name__ == '__main__':
	main()