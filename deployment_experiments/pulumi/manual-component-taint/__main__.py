"""A Python Pulumi program"""

import os
import pulumi
from pulumi import Input
from pulumi import Output
from pulumi import ResourceOptions
from pulumi_random import RandomUuid
from pulumi_command.local import Command


class RandomUUIDWithPrefix(pulumi.ComponentResource):
	def __init__(self, resource_name: str, prefix_for_random: Input[str], opts: ResourceOptions | None = None):
		super().__init__(t="requiem:experiments:RandomUUIDWithPrefix", props={"prefix_for_random": prefix_for_random}, name=resource_name, opts=opts)
		if os.environ.get("force_failure", "") == "true":
			command_string = "exit 1"
		else:
			command_string = "exit 0"
		self._prefix_for_random = prefix_for_random
		self._base_random_uuid = RandomUuid(f"{resource_name}-random-uuid", opts=ResourceOptions(parent=self))
		# self._pass_or_fail_command = Command(
		# 	f"{resource_name}-pass-or-fail",
		# 	opts=ResourceOptions(depends_on=self._)
		# )
		self.register_outputs({"value": self.value})

	@property
	def value(self) -> Output[str]:
		return Output.concat(self._prefix_for_random, self._base_random_uuid.result)


uuid_with_prefix = RandomUUIDWithPrefix(
	"resource_name",
	prefix_for_random="12345-",
	opts=ResourceOptions())
pulumi.export("random_value", uuid_with_prefix.value)
