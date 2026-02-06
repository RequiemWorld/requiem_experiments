import unittest
from structureipc import Structure
from structureipc import LongField


class TestSingleLongSize(unittest.TestCase):

    def test_should_report_size_of_structure_with_one_long_as_8_bytes(self):
        class SingleLongStructure(Structure):
            single_long: int = LongField()
        self.assertEqual(8, SingleLongStructure.size)


class TestMultipleLongSize(unittest.TestCase):
    def test_should_report_size_of_structure_with_three_longs_as_24_bytes(self):
        class ThreeLongStructure(Structure):
            long_one: int = LongField()
            long_two: int = LongField()
            long_three: int = LongField()
        self.assertEqual(24, ThreeLongStructure.size)