import unittest
from structureipc import Structure, LongField


class SingleLongStructure(Structure):
    single_long: int = LongField()


class TestConstructingWithSingleLong(unittest.TestCase):

    def test_should_construct_class_with_single_long_as_expected(self):
        class MyStructure(Structure):
            some_number: int = LongField()
        structure_object = MyStructure(some_number=5)
        self.assertEqual(5, structure_object.some_number)

    def test_should_construct_object_with_single_long_and_report_size_as_8_bytes(self):
        structure_object = SingleLongStructure(single_long=1234)
        self.assertEqual(8, structure_object.size)


class TestConstructingWithMultipleLongs(unittest.TestCase):
    def test_should_construct_object_with_three_longs_and_report_size_as_24_bytes(self):
        class ThreeLongStructure(Structure):
            long_one: int = LongField()
            long_two: int = LongField()
            long_three: int = LongField()
        structure_object = ThreeLongStructure(long_one=1, long_two=2, long_three=3)
        self.assertEqual(24, structure_object.size)
