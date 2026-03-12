import unittest
from speedtest import LoadRunner, SpeedTestResult
from speedtest import SpeedTest


class LoadRunnerTestFixture(unittest.IsolatedAsyncioTestCase):
    _load_runner: LoadRunner

    async def asyncSetUp(self):
        self._dummy_target_execution_count = 0
        self._dummy_target_error_to_raise = None

        async def dummy():
            self._dummy_target_execution_count += 1
            if self._dummy_target_error_to_raise is not None:
                raise self._dummy_target_error_to_raise
        self._load_runner = LoadRunner(target=dummy)

    @staticmethod
    def assertAllResultsExecutedWithinOneSecond(results: list[SpeedTestResult]):
        # AI generated implementation
        if not results:
            raise AssertionError("No results to check")

        # convert start times to seconds
        start_times = [r.start_time_nanoseconds / 1_000_000_000 for r in results]

        # find the earliest start time as the batch reference
        batch_start = min(start_times)

        for r in results:
            start_secs = r.start_time_nanoseconds / 1_000_000_000
            finish_secs = r.finish_time_nanoseconds / 1_000_000_000

            if not (batch_start <= start_secs < batch_start + 1):
                raise AssertionError(
                    f"Result started outside 1-second window: {start_secs} vs batch_start {batch_start}"
                )

            if not (batch_start <= finish_secs < batch_start + 1):
                raise AssertionError(
                    f"Result finished outside 1-second window: {finish_secs} vs batch_start {batch_start}"
                )