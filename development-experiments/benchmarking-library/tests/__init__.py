import queue


class FakeNanosecondTimeProvider:

	def __init__(self):
		self._reporting_queue: queue.Queue[int] = queue.Queue()

	def __call__(self, *args, **kwargs) -> int:
		if self._reporting_queue.empty():
			raise Exception

		return self._reporting_queue.get()

	def clear_sequence_queue(self):
		self._reporting_queue = queue.Queue()

	def sequence_nanoseconds(self, amount: int) -> None:
		self._reporting_queue.put(amount)
