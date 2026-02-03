import unittest
from experiment.ring_buffer import LongRingBuffer
from multiprocessing.shared_memory import SharedMemory



class RingBufferTestCase(unittest.TestCase):
	def setUp(self):
		capacity = 16  # 16 longs
		self._capacity = capacity
		head_and_tail = 16  # two longs at the beginning + maybe 56 byte padding for each in the future
		long_capacity_size = capacity * 8  # 16 longs
		shared_memory_size = head_and_tail + long_capacity_size
		self._shared_memory = SharedMemory(name="shared_memory", size=shared_memory_size, create=True)
		self._ring_buffer = LongRingBuffer(self._shared_memory, capacity)

	def tearDown(self):
		self._shared_memory.unlink()
		self._shared_memory.close()


class TestRingBufferWrapping(RingBufferTestCase):

	def test_should_rewrite_first_slot_when_writing_past_end_of_buffer(self):
		for _ in range(self._capacity):
			self._ring_buffer.put(10)
		self._ring_buffer.put(20)
		self.assertEqual(20, self._ring_buffer.get())
		self.assertEqual(10, self._ring_buffer.get())

class TestRingBufferGettingAndPutting(RingBufferTestCase):

	def test_get_should_return_none_initially_when_nothing_put_in_buffer(self):
		self.assertIsNone(self._ring_buffer.get())

	def test_get_should_return_single_long_put_into_buffer_after(self):
		self._ring_buffer.put(50)
		self.assertEqual(50, self._ring_buffer.get())

	def test_get_should_return_multiple_added_values_in_order_correctly(self):
		self._ring_buffer.put(50)
		self._ring_buffer.put(80)
		self.assertEqual(50, self._ring_buffer.get())
		self.assertEqual(80, self._ring_buffer.get())

