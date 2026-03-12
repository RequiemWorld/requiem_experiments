import time
import numpy
import asyncio
from dataclasses import dataclass
from typing import Callable


@dataclass
class SpeedTestResult:
    start_time_nanoseconds: int
    finish_time_nanoseconds: int
    error_encountered: Exception | None = None

    @property
    def time_taken_nanoseconds(self) -> int:
        return self.finish_time_nanoseconds - self.start_time_nanoseconds

    @property
    def time_taken_milliseconds(self) -> float:
        return (self.finish_time_nanoseconds - self.start_time_nanoseconds) / 1_000_000


class SpeedTest:
    def __init__(self, target, on_completion: Callable[[SpeedTestResult], None]):
        self._target = target
        self._on_completion = on_completion

    async def execute(self) -> SpeedTestResult:
        start_time_nanoseconds = time.time_ns()
        try:
            await self._target()
            error_encountered = None
        except Exception as e:
            error_encountered = e

        finish_time_nanoseconds = time.time_ns()
        speed_test_result = SpeedTestResult(start_time_nanoseconds, finish_time_nanoseconds, error_encountered)
        self._on_completion(speed_test_result)
        return speed_test_result


@dataclass
class LoadRunResult:
    speed_test_results: list[SpeedTestResult]
    minimum_execution_ms: int
    maximum_execution_ms: int
    percentile_99_9999: float
    error_count: int
    execution_count: int


class ResultTracker:
    def __init__(self):
        self._speed_test_results = []
        self._error_count = 0
        self._execution_count = 0

    def track_speed_test_result(self, result: SpeedTestResult):
        self._speed_test_results.append(result)
        self._execution_count += 1
        if result.error_encountered is not None:
            self._error_count += 1

    def compute_result(self) -> LoadRunResult:
        execution_times_ms = [result.time_taken_milliseconds for result in self._speed_test_results]
        percentile_99_9999 = float(numpy.percentile(execution_times_ms, 99.9999))
        return LoadRunResult(
            speed_test_results=self._speed_test_results,
            minimum_execution_ms=int(min(execution_times_ms)),
            maximum_execution_ms=int(max(execution_times_ms)),
            error_count=self._error_count,
            percentile_99_9999=percentile_99_9999,
            execution_count=self._execution_count)


class LoadRunner:
    def __init__(self, target):
        self._target = target
        self._created_tasks: list[asyncio.Task[SpeedTest]] = []
        self.arrival_rate: int = 10
        self.run_duration: float = 2

    async def _wait_for_tasks_to_finish(self) -> None:
        await asyncio.gather(*self._created_tasks)

    async def execute(self) -> LoadRunResult:
        result_tracker = ResultTracker()

        def _on_speed_test_completion(result: SpeedTestResult) -> None:
            result_tracker.track_speed_test_result(result)

        start_time = time.time()
        while time.time() - start_time < self.run_duration:
            for _ in range(self.arrival_rate):
                speed_test = SpeedTest(self._target, on_completion=_on_speed_test_completion)
                task = asyncio.create_task(speed_test.execute())
                self._created_tasks.append(task)
            await asyncio.sleep(1)
        await self._wait_for_tasks_to_finish()
        return result_tracker.compute_result()
