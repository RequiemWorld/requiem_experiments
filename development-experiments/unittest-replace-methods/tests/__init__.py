import unittest
from typing import Type, Any


def _find_method_names_on_class(class_: Type[Any]) -> list[str]:
	method_attribute_names = []
	for attribute_name in dir(class_):
		attribute_value = getattr(class_, attribute_name)
		if callable(attribute_value):
			method_attribute_names.append(attribute_name)
	return method_attribute_names


def _replace_method_with_another(class_: Type[Any], method_name: str, new_method) -> str:
	setattr(class_, method_name, new_method)


class AlwaysFailTestCase(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def __init_subclass__(cls):
		method_names_on_class = _find_method_names_on_class(cls)
		for method_name in method_names_on_class:
			method_is_test = method_name.startswith("test")
			if method_is_test:
				original_method = getattr(cls, method_name)
				def always_fail_method(self: AlwaysFailTestCase):
					original_method(self)
					self.fail("you've inherited AlwaysFailTestCase, it's always going to fail anyway after executing")
				always_fail_method = always_fail_method
				_replace_method_with_another(cls, method_name, always_fail_method)
