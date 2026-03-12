import unittest
from speedtest import ResultTracker
from speedtest import SpeedTestResult


class TestResultTrackerPercentiles(unittest.TestCase):
    def setUp(self):
        self._result_tracker = ResultTracker()

    def test_should_compute_99_9999_millisecond_percentile_latency_correctly(self):
        result_1 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=2000000)
        result_2 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=3000000)
        result_3 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=4000000)
        self._result_tracker.track_speed_test_result(result_1)
        self._result_tracker.track_speed_test_result(result_2)
        self._result_tracker.track_speed_test_result(result_3)
        self.assertEqual(3.9999979999999997, self._result_tracker.compute_result().percentile_99_9999)


class TestResultTracker(unittest.TestCase):
    def setUp(self):
        self._result_tracker = ResultTracker()

    def test_should_compute_result_correctly_regarding_error_count(self):
        result_1 = SpeedTestResult(start_time_nanoseconds=1, finish_time_nanoseconds=2, error_encountered=Exception())
        result_2 = SpeedTestResult(start_time_nanoseconds=1, finish_time_nanoseconds=2, error_encountered=Exception())
        self._result_tracker.track_speed_test_result(result_1)
        self._result_tracker.track_speed_test_result(result_2)
        self.assertEqual(2, self._result_tracker.compute_result().error_count)

    def test_should_compute_result_correctly_regarding_millisecond_execution_time(self):
        result_1 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=1000000)
        result_2 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=2000000)
        self._result_tracker.track_speed_test_result(result_1)
        self._result_tracker.track_speed_test_result(result_2)
        result = self._result_tracker.compute_result()
        self.assertEqual(1, result.minimum_execution_ms)
        self.assertEqual(2, result.maximum_execution_ms)

    def test_should_compute_result_correctly_regarding_execution_count(self):
        result_1 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=1)
        result_2 = SpeedTestResult(start_time_nanoseconds=0, finish_time_nanoseconds=2)
        self._result_tracker.track_speed_test_result(result_1)
        self._result_tracker.track_speed_test_result(result_2)
        self.assertEqual(2, self._result_tracker.compute_result().execution_count)
