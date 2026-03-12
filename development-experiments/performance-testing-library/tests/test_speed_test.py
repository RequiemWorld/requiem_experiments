import time
import asyncio
from unittest import IsolatedAsyncioTestCase
from speedtest import SpeedTest


class TestSpeedTestErrorHandling(IsolatedAsyncioTestCase):
    async def test_should_return_result_containing_error_raised_by_target(self):
        async def _target_which_raises_error():
            raise NotImplementedError
        speed_test = SpeedTest(_target_which_raises_error, lambda x: None)
        speed_test_result = await speed_test.execute()
        self.assertIsInstance(speed_test_result.error_encountered, NotImplementedError)


class TestSpeedTestTimeMeasurement(IsolatedAsyncioTestCase):
    # things are not fast enough on pypy for this test to work
    async def test_should_return_result_with_accurate_enough_millisecond_execution_time(self):
        async def _sleep_for_15_milliseconds():
            time.sleep(0.015)
        speed_test = SpeedTest(target=_sleep_for_15_milliseconds, on_completion=lambda x: None)
        speed_test_result = await speed_test.execute()
        self.assertEqual(15, int(speed_test_result.time_taken_milliseconds))

