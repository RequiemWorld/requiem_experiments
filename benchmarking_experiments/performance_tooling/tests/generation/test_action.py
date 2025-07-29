import time
import queue
import unittest
from datetime import datetime
from datetime import timedelta
from perftooling.generation import Action

class TimestampMaker:

	def __init__(self, base_timestamp: float):
		self._current_timestamp = base_timestamp

	def add_milliseconds(self, milliseconds: int) -> None:
		self._current_timestamp += milliseconds / 1000

	def add_seconds(self, seconds: int) -> None:
		self._current_timestamp += seconds

	def make_timestamp(self) -> float:
		return self._current_timestamp


class SequencedTimeFunctionMock:
	def __init__(self):
		self._sequenced_timestamps: queue.Queue[float] = queue.Queue()

	def __call__(self) -> float:
		"""
		:raises RuntimeError: When there are no more sequenced times to grab from.
		"""
		if self._sequenced_timestamps.empty():
			raise RuntimeError()
		return self._sequenced_timestamps.get()

	def sequence_timestamp(self, timestamp: float) -> None:
		self._sequenced_timestamps.put(timestamp)


class ActionTestFixture(unittest.IsolatedAsyncioTestCase):
	def setUp(self):
		self._time_to_provide = datetime(2000, 1, 2).timestamp()
		self._timestamp_maker = TimestampMaker(datetime(2000, 1, 2).timestamp())
		self._time_function_mock = SequencedTimeFunctionMock()

	def addSecondsToTime(self, seconds: int):
		self._time_to_provide += timedelta(seconds=seconds).total_seconds()

	def addMinutesToTime(self, minutes: int):
		self._time_to_provide += timedelta(minutes=minutes).total_seconds()

	def addMillisecondsToTime(self, milliseconds: int):
		self._time_to_provide += timedelta(milliseconds=milliseconds).total_seconds()


class TestActionExecutionExecutingAwaitable(ActionTestFixture):
	async def test_should_execute_the_awaitable_by_awaiting_it(self):
		was_executed: bool = False
		async def _execute_me():
			nonlocal was_executed
			was_executed = True
		self.assertFalse(was_executed)
		action = Action(_execute_me(), time.time)
		await action.execute()
		self.assertTrue(was_executed)


class TestActionExecutionTimeAccuracy(ActionTestFixture):
	async def test_should_report_as_only_taking_one_millisecond_correctly(self):
		async def _dummy_coroutine(): pass
		action = Action(_dummy_coroutine(), self._time_function_mock)
		self._time_function_mock.sequence_timestamp(self._timestamp_maker.make_timestamp())
		self._timestamp_maker.add_milliseconds(1)
		self._time_function_mock.sequence_timestamp(self._timestamp_maker.make_timestamp())
		await action.execute()
		self.assertEqual(1, action.execution_time_in_milliseconds)

	async def test_should_report_multiple_seconds_taken_in_milliseconds_correctly(self):
		async def _dummy_coroutine(): pass
		action = Action(_dummy_coroutine(), self._time_function_mock)

		self._time_function_mock.sequence_timestamp(self._timestamp_maker.make_timestamp())
		self._timestamp_maker.add_seconds(5)
		self._time_function_mock.sequence_timestamp(self._timestamp_maker.make_timestamp())
		await action.execute()
		self.assertEqual(5000, action.execution_time_in_milliseconds)
