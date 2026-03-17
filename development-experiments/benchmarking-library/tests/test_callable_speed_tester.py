import unittest
from speedtest import CallableSpeedTester
from . import FakeNanosecondTimeProvider


class TestCallableSpeedTester(unittest.TestCase):
	def setUp(self):
		self._time_provider = FakeNanosecondTimeProvider()
		self._time_provider.sequence_nanoseconds(0)
		self._speed_tester = CallableSpeedTester(self._time_provider)

	def test_should_measure_nanoseconds_taken_correctly_for_second_range(self):
		self._time_provider.sequence_nanoseconds(2000000000)
		self.assertEqual(2000000000, self._speed_tester.execute(lambda: None))

	def test_should_measure_nanoseconds_taken_correctly_for_nanosecond_range(self):
		self._time_provider.sequence_nanoseconds(5)
		self.assertEqual(5, self._speed_tester.execute(lambda: None))

	def test_should_execute_callable_given_in_execute_method(self):
		self._time_provider.sequence_nanoseconds(5)
		self.assertEqual(5, self._speed_tester.execute(lambda: None))
