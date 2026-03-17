import unittest
from speedtest import BenchmarkResult
from speedtest import PresentableBenchmarkResult


class BenchmarkResultConversion(unittest.TestCase):
	def setUp(self):
		self._benchmark_result = BenchmarkResult(
			minimum_nanoseconds=11_000,
			maximum_nanoseconds=12_000,
			mean_nanoseconds=13_000,
			p99_nanoseconds=14_000,
			p99_99_nanoseconds=15_000,
			standard_deviation=16_000)

	def test_should_convert_to_presentable_result_with_commas_in_minimum_nanoseconds_number(self):
		self.assertEqual("11,000", self._benchmark_result.to_presentable_result().minimum_nanoseconds)

	def test_should_convert_to_presentable_result_with_commas_in_maximum_nanoseconds_number(self):
		self.assertEqual("12,000", self._benchmark_result.to_presentable_result().maximum_nanoseconds)

	def test_should_convert_to_presentable_result_with_commas_in_mean_nanoseconds_number(self):
		self.assertEqual("13,000", self._benchmark_result.to_presentable_result().mean_nanoseconds)

	def test_should_convert_to_presentable_result_with_commas_in_p99_nanoseconds_number(self):
		self.assertEqual("14,000", self._benchmark_result.to_presentable_result().p99_nanoseconds)

	def test_should_convert_to_presentable_result_with_commas_in_p99_99_nanoseconds_number(self):
		self.assertEqual("15,000", self._benchmark_result.to_presentable_result().p99_99_nanoseconds)

	def test_should_convert_to_presentable_result_with_commas_in_standard_deviation_number(self):
		self.assertEqual("16,000", self._benchmark_result.to_presentable_result().standard_deviation)
