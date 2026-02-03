import multiprocessing
from multiprocessing import Queue


# Single Producer/Single Consumer worker
class IncrementWorker:
	def __init__(self, request_queue: Queue, response_queue: Queue):
		self._request_queue = request_queue
		self._response_queue = response_queue
		self._current_number = 0

	def execute(self) -> None:
		while True:
			number_to_increment_by = self._request_queue.get()
			self._current_number += number_to_increment_by
			self._response_queue.put(self._current_number)


class IncrementHelper:
	def __init__(self, request_queue: Queue, response_queue: Queue):
		self._request_queue = request_queue
		self._response_queue = response_queue

	def increment_number(self, by_amount: int) -> int:
		self._request_queue.put(by_amount)
		return self._response_queue.get()

