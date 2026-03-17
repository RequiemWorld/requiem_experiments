import os
import psutil
import unittest
import multiprocessing
from speedtest import BenchmarkHarnessCallableExecutor


class TestBenchmarkCallableExecutor(unittest.TestCase):
	def setUp(self):
		self._executor = BenchmarkHarnessCallableExecutor()

	def _get_cpu_affinity(self) -> list[int]:
		return psutil.Process(os.getpid()).cpu_affinity()

	def test_should_execute_callable_in_different_process(self):
		result_queue = multiprocessing.Queue()
		def target_callable():
			result_queue.put(os.getpid())
		self._executor.execute_callable(target_callable, [])
		self.assertNotEqual(os.getpid(), result_queue.get())

	def test_should_execute_callable_and_pass_on_return_value(self):
		def target_callable():
			return 5
		self.assertEqual(5, self._executor.execute_callable(target_callable, []))

	def test_should_execute_callable_and_pass_on_any_exceptions(self):
		def target_callable():
			raise RuntimeError
		with self.assertRaises(Exception):
			self._executor.execute_callable(target_callable, [])

	# this is only going to work if the machine has at least 2 cores.
	def test_should_execute_callable_with_process_pinned_to_one_given_cpu_core(self):
		def target_callable():
			return self._get_cpu_affinity()
		result = self._executor.execute_callable(target_callable, [1])  # actually core 2
		self.assertEqual([1], result)

	# this is only going to work if the machine has at least 4 cores (public GitHub runners will suffice)
	def test_should_execute_callable_with_process_pinned_to_multiple_given_cpu_cores(self):
		def target_callable():
			return self._get_cpu_affinity()
		result = self._executor.execute_callable(target_callable, [1, 2])  # cores 2 and 3
		self.assertEqual([1, 2], result)

	def test_should_execute_callable_with_all_cores_available_when_none_specified(self):
		def target_callable():
			return self._get_cpu_affinity()
		result = self._executor.execute_callable(target_callable, [])  # cores 2 and 3
		self.assertEqual(self._get_cpu_affinity(), result)
