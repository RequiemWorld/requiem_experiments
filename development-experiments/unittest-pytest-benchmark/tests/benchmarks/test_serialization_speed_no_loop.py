import struct
from benchcase import BenchCase


class TestSerializationSpeed(BenchCase):

	def test_speed_of_struct_pack_for_little_endian_long(self):
		struct.pack("q", 0xFFFFFFFFFF)

	def test_speed_of_int_to_bytes_for_little_endian_long(self):
		(0xFFFFFFFFFF).to_bytes(8, byteorder="little")
