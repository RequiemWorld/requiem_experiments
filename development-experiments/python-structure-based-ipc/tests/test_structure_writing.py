import unittest
from structureipc import Structure, LongField


class TestSingleLongWriting(unittest.TestCase):

    def test_should_write_struct_with_only_a_long_into_somewhere_correctly(self):
        class SingleLongStructure(Structure):
            single_long: int = LongField()
        buffer = bytearray(8)
        buffer[0:8] = b"\xee" * 8
        SingleLongStructure(single_long=5).write_into(buffer)
        self.assertEqual(b"\x05\x00\x00\x00\x00\x00\x00\x00", buffer[0:8])
