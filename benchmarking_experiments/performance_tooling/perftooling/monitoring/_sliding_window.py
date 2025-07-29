from typing import Callable
from collections import deque


class SlidingWindowActionsPerSecondMonitor:
	"""
	An object that is able to track the number of actions that have happened
	in the past second, not resetting to zero after every second, tracking accurately.
	"""
	def __init__(self, tracking_capacity: int, timestamp_provider: Callable[[], float]):
		"""
		:param tracking_capacity: This is the limit for timestamps of actions that can be stored, it is impossible to monitor more actions per second than this.
		:param timestamp_provider: A callable that will provide a float of the given timestamp in the same format as time.time would.
		"""
		self._tracking_capacity = tracking_capacity
		self._timestamp_buffer = deque(maxlen=tracking_capacity)
		self._timestamp_provider = timestamp_provider

	def notify_of_action(self) -> None:
		self._timestamp_buffer.append(self._timestamp_provider())

	def get_actions_per_second(self) -> int:
		time_one_second_ago = self._timestamp_provider() - 1
		amount_since_one_second_ago = 0
		for time_entry in self._timestamp_buffer:
			if time_entry > time_one_second_ago:
				amount_since_one_second_ago += 1
		return amount_since_one_second_ago