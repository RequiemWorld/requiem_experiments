import struct
from benchcase import BenchCase


class MyBenchmark(BenchCase):
	def setUp(self):
		self._serialization_numbers = range(1, 1000000)

	def test_serialization_speed_of_1000000_numbers_individually_as_long_with_struct_pack(self):
		for number in self._serialization_numbers:
			struct.pack("q", number)

	def test_serialization_speed_of_1000000_numbers_individually_as_long_with_int_to_bytes(self):
		for number in self._serialization_numbers:
			number.to_bytes(8, "little")
