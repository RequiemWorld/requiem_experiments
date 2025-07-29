import unittest
import datetime
from datetime import timedelta
from perftooling.monitoring import SlidingWindowActionsPerSecondMonitor


class SlidingWindowAPSMonitorTestFixture(unittest.TestCase):
	def setUp(self):
		self._time_to_provide = datetime.datetime(1991, 1, 2).timestamp()
		self._time_provider = lambda: self._time_to_provide
		self._monitor = SlidingWindowActionsPerSecondMonitor(16000, self._time_provider)

	def addSecondsToTime(self, seconds: int):
		self._time_to_provide += timedelta(seconds=seconds).total_seconds()

	def addMinutesToTime(self, minutes: int):
		self._time_to_provide += timedelta(minutes=minutes).total_seconds()

	def addMillisecondsToTime(self, milliseconds: int):
		self._time_to_provide += timedelta(milliseconds=milliseconds).total_seconds()


class TestAPSMonitorSimpleReporting(SlidingWindowAPSMonitorTestFixture):
	def test_should_report_zero_for_actions_per_second_when_never_notified(self):
		self.assertEqual(0, self._monitor.get_actions_per_second())

	def test_should_report_one_for_actions_per_second_after_being_notified_once_in_last_second(self):
		self._monitor.notify_of_action()
		self.assertEqual(1, self._monitor.get_actions_per_second())

	def test_should_be_able_to_monitor_hypothetical_one_thousand_actions_in_one_second(self):
		# This is a test for logic, not performance/the constraints of python.
		for _ in range(1000):
			self._monitor.notify_of_action()
		self.assertEqual(1000, self._monitor.get_actions_per_second())

	def test_should_report_zero_for_actions_per_second_after_a_second_from_only_one_request_before(self):
		self._monitor.notify_of_action()
		self.assertEqual(1, self._monitor.get_actions_per_second())
		self.addSecondsToTime(1)
		self.assertEqual(0, self._monitor.get_actions_per_second())

# When a second passes, the amount of requests reported shouldn't drop to zero,
# I think this is called a sliding window or something.
class TestRPSMonitorSlidingWindowReporting(SlidingWindowAPSMonitorTestFixture):
	def test_should_have_simple_sliding_window_logic(self):
		# If I notify the monitor of a action, and 900 milliseconds go by
		self._monitor.notify_of_action()
		self.addMillisecondsToTime(900)
		# and I notify the monitor of two more actions instantly
		self._monitor.notify_of_action()
		self._monitor.notify_of_action()
		# and a total of a second has passed since the first notification
		self.addMillisecondsToTime(100)
		# then the amount of actions per second at the time asked for should be two.
		self.assertEqual(2, self._monitor.get_actions_per_second())
