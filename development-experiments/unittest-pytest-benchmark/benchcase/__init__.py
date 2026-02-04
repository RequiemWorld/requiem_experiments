import pytest
import unittest
from typing import Type, Any


def _find_method_names_on_class(class_: Type[Any]) -> list[str]:
	method_attribute_names = []
	for attribute_name in dir(class_):
		attribute_value = getattr(class_, attribute_name)
		if callable(attribute_value):
			method_attribute_names.append(attribute_name)
	return method_attribute_names


def _find_test_method_names_on_class(class_: Type):
	test_method_names = []
	for method_name in _find_method_names_on_class(class_):
		if method_name.startswith("test"):
			test_method_names.append(method_name)
	return test_method_names


def _replace_method_with_another(clazz: Type, method_name: str, new_method) -> None:
	setattr(clazz, method_name, new_method)


class BenchCase(unittest.TestCase):
	__benchmark: Any

	def __init_subclass__(cls, **kwargs):
		# this will replace the original methods before they're collected,
		# we don't have the benchmark callable to use in the replaced method yet.
		test_method_names = _find_test_method_names_on_class(cls)
		for test_method_name in test_method_names:
			original_method = getattr(cls, test_method_name)
			def replacement_method(self: BenchCase):
				# I think we might need to run setup/teardown before each run?
				# not sure if it is better to use pedantic here or not.
				self.__benchmark(lambda: original_method)
			_replace_method_with_another(cls, test_method_name, replacement_method)

	@pytest.fixture(autouse=True, scope="function")
	def __fixture_thing(self, benchmark):
		# We have the benchmark callable and the replaced methods from earlier will use it on our original.
		self.__benchmark = benchmark



