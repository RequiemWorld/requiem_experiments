import multiprocessing
import typing
from typing import Callable
from dataclasses import dataclass
from hdrh.histogram import HdrHistogram


class CallableSpeedTester:
	def __init__(self, nanosecond_time_provider: Callable[[], int]):
		self._ns_time_provider = nanosecond_time_provider

	def execute(self, callable_: Callable) -> int:
		ns_start = self._ns_time_provider()
		callable_()
		ns_finish = self._ns_time_provider()
		return ns_finish - ns_start


@dataclass
class PresentableBenchmarkResult:
	minimum_nanoseconds: str
	maximum_nanoseconds: str
	mean_nanoseconds: str
	p99_nanoseconds: str
	p99_99_nanoseconds: str
	standard_deviation: str

	def print_result_in_table(self) -> None:
		raise NotImplementedError


@dataclass
class BenchmarkResult:
	minimum_nanoseconds: int
	maximum_nanoseconds: int
	mean_nanoseconds: float
	p99_nanoseconds: int
	p99_99_nanoseconds: int
	standard_deviation: int

	def to_presentable_result(self) -> PresentableBenchmarkResult:

		return PresentableBenchmarkResult(
			f"{self.minimum_nanoseconds:,}",
			f"{self.maximum_nanoseconds:,}",
			f"{self.mean_nanoseconds:,}",
			f"{self.p99_nanoseconds:,}",
			f"{self.p99_99_nanoseconds:,}",
			f"{self.standard_deviation:,}")


class CallableBenchmarker:
	def __init__(self, speed_tester: CallableSpeedTester):
		self._speed_tester = speed_tester

	def benchmark_callable(self, callable_: Callable, iterations: int):
		histogram = HdrHistogram(1, 1_000_000_000, 3)
		for _ in range(iterations):
			nanoseconds_taken = self._speed_tester.execute(callable_)
			histogram.record_value(nanoseconds_taken)
		benchmark_result = BenchmarkResult(
			minimum_nanoseconds=histogram.get_min_value(),
			maximum_nanoseconds=histogram.get_max_value(),
			mean_nanoseconds=histogram.get_mean_value(),
			p99_nanoseconds=histogram.get_value_at_percentile(99),
			p99_99_nanoseconds=histogram.get_value_at_percentile(99.99),
			standard_deviation=histogram.get_stddev())
		return benchmark_result


from dataclasses import dataclass
class BenchmarkHarnessOptions:
	pin_cpu_cores: int | None = None


class BenchmarkHarnessCallableExecutor:

	def execute_callable(self, callable_: Callable, cpu_cores: list[int]) -> typing.Any:  # FIXME use proper type later
		"""
		Executes a callable on specific CPU cores by spawning a new process
		and pinning it to the provided CPU Cores.
		"""
		result_queue = multiprocessing.Queue()
		def proxy_call_and_capture_result():
			try:
				result = callable_()
			except Exception as e:
				result = e
			result_queue.put(result)
		process = multiprocessing.Process(target=proxy_call_and_capture_result)
		process.start()
		result_of_callable = result_queue.get()
		if isinstance(result_of_callable, Exception):
			raise result_of_callable
		return result_of_callable


class BenchmarkHarness:
	def __init__(self, cpu_cores: int):
		self._cpu_cores = cpu_cores

	def benchmark_callable(self):
		raise NotImplementedError