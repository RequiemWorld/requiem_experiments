import unittest
from ._import_helper import *
from pulumi_helper import check_that_no_resources_changed


class TestResourceChangeCheckingFunction(unittest.TestCase):

	def test_should_raise_value_error_when_given_empty_mapping(self):
		with self.assertRaises(ValueError):
			check_that_no_resources_changed({})

	def test_should_return_false_when_anything_other_than_same_is_in_given_mapping(self):
		self.assertFalse(check_that_no_resources_changed({"anything1": 1, "anything2": 2}))

	def test_should_return_true_when_there_is_same_and_nothing_else_in_given_mapping(self):
		self.assertTrue(check_that_no_resources_changed({"same": 1}))

	def test_should_return_false_when_there_is_same_and_anything_else_in_given_mapping(self):
		self.assertFalse(check_that_no_resources_changed({"same": 1, "thing": 1}))
