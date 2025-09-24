from typing import Mapping
from ._intervention import drop_into_ssh


def check_that_no_resources_changed(resource_changes: Mapping[str, int]) -> bool:
	"""
	Verifies that there are no changes to any resources based on
	what's in the given resource_changes dictionary.

	:raises ValueError: When there are no keys in the mapping.
	"""
	# When the stack is first brought up, it will have {"create": number},
	# When the stack is 'brought up' again and nothing changes, there will be a {"same": number_of_resources}
	if not resource_changes.keys():
		raise ValueError("there are no keys in the changes. this isn't possible in our limited knowledge of pulumi.")

	has_key_of_same = "same" in resource_changes
	has_keys_of_anything_other_than_same = any(key for key in resource_changes if key != "same")
	return has_key_of_same and not has_keys_of_anything_other_than_same


