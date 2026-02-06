import unittest
from structureipc import FieldType
from structureipc import LongField
from structureipc import read_fields_from_class


class TestReadingLongField(unittest.TestCase):

    def test_should_read_long_field_from_class_with_it_set_explicitly(self):
        class ExampleClass:
            my_field: int = LongField()
        fields = read_fields_from_class(ExampleClass)
        first_field = fields[0]
        self.assertEqual(FieldType.LONG, first_field.type)

    def test_should_fill_in_name_of_long_field_when_set_explicitly(self):
        class ExampleClass:
            field_name1: int = LongField()
        self.assertEqual("field_name1", read_fields_from_class(ExampleClass)[0].name)
