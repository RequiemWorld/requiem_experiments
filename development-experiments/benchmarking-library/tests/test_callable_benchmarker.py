import unittest
from . import FakeNanosecondTimeProvider
from speedtest import CallableSpeedTester
from speedtest import CallableBenchmarker


class TestCallableBenchmarker(unittest.TestCase):

	def setUp(self):
		self._time_provider = FakeNanosecondTimeProvider()
		self._callable_benchmarker = CallableBenchmarker(CallableSpeedTester(self._time_provider))

	def _enqueue_nanosecond_call_duration(self, duration_ns: int) -> None:
		self._time_provider.sequence_nanoseconds(0)
		self._time_provider.sequence_nanoseconds(duration_ns)

	def test_should_measure_minimum_time_taken_correctly(self):
		# first iteration will take 10 nanoseconds
		self._enqueue_nanosecond_call_duration(10)
		# second iteration will take 5 nanoseconds
		self._enqueue_nanosecond_call_duration(5)
		# second iteration will take 20 nanoseconds
		self._enqueue_nanosecond_call_duration(20)
		result = self._callable_benchmarker.benchmark_callable(lambda: None, 3)
		self.assertEqual(5, result.minimum_nanoseconds)

	def test_should_measure_maximum_time_taken_correctly(self):
		self._enqueue_nanosecond_call_duration(10)
		self._enqueue_nanosecond_call_duration(20)
		self._enqueue_nanosecond_call_duration(300)
		self._enqueue_nanosecond_call_duration(40)
		result = self._callable_benchmarker.benchmark_callable(lambda: None, 4)
		self.assertEqual(300, result.maximum_nanoseconds)

	def test_should_measure_mean_time_taken_correctly(self):
		self._enqueue_nanosecond_call_duration(50)
		self._enqueue_nanosecond_call_duration(152)
		self._enqueue_nanosecond_call_duration(333)
		self._enqueue_nanosecond_call_duration(111)
		result = self._callable_benchmarker.benchmark_callable(lambda: None, 4)
		# >>> statistics.mean([50, 152, 333, 111])
		# 161.5
		self.assertEqual(161.5, result.mean_nanoseconds)