import struct
from multiprocessing.shared_memory import SharedMemory


# A hardcoded, single producer, single consumer ring buffer,
# with the responsibility of reading the next items with get, like a queue.
class LongRingBuffer:

	def __init__(self, memory: SharedMemory, capacity: int):
		self._buffer = memory.buf
		self._capacity = capacity
		self._entries_offset = 16

	@staticmethod
	def make_shared_memory(name: str, capacity: int) -> SharedMemory:
		memory = SharedMemory(name=name, create=True, size=capacity * 8 + 16)
		return memory

	def _get_tail_index(self) -> int:
		return struct.unpack_from("q", self._buffer, offset=0)[0]

	def _get_head_index(self) -> int:
		return struct.unpack_from("q", self._buffer, offset=8)[0]

	def _write_into_slot(self, slot: int, long: int) -> None:
		# It probably would make this a lot simpler to put the entries
		# at the beginning and the head/tail at the end.
		entry_size = 8
		slot_write_offset = self._entries_offset + entry_size * slot
		struct.pack_into("q", self._buffer, slot_write_offset, long)

	def _read_from_slot(self, slot: int) -> int:
		entry_size = 8
		slot_read_offset = self._entries_offset + entry_size * slot
		return struct.unpack_from("q", self._buffer, slot_read_offset)[0]

	def _bump_tail_index(self) -> None:
		# The tail index is the slot that is supposed to be read next.
		old_head_index = struct.unpack_from("q", self._buffer, offset=0)[0]
		struct.pack_into("q", self._buffer, 0, old_head_index + 1)

	def _bump_head_index(self) -> int:
		old_head_index = struct.unpack_from("q", self._buffer, offset=8)[0]
		struct.pack_into("q", self._buffer, 8, old_head_index + 1)

	def put(self, long: int) -> None:
		slot_to_write_into = self._get_head_index()
		self._write_into_slot(slot_to_write_into % self._capacity, long)
		self._bump_head_index()

	def get(self) -> int | None:
		tail_index = self._get_tail_index()
		head_index = self._get_head_index()
		if tail_index < head_index:
			long_value = self._read_from_slot(tail_index)
			self._bump_tail_index()
			return long_value
		return None


class IncrementWorker:
	def __init__(self, request_buffer: LongRingBuffer, response_buffer: LongRingBuffer):
		self._request_buffer = request_buffer
		self._response_buffer = response_buffer
		self._current_number = 0

	def execute(self) -> None:
		while True:
			increment_by = self._request_buffer.get()
			if increment_by is not None:
				self._current_number += increment_by


class IncrementHelper:
	def __init__(self, request_buffer: LongRingBuffer, response_buffer: LongRingBuffer):
		self._request_buffer = request_buffer
		self._response_buffer = response_buffer

	def increment_number(self, by_amount: int) -> int:
		self._request_buffer.put(by_amount)
		return self._response_buffer.get()
