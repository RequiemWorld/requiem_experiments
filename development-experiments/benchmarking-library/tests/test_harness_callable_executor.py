import os
import unittest
import multiprocessing
from speedtest import BenchmarkHarnessCallableExecutor


class TestBenchmarkCallableExecutor(unittest.TestCase):
	def setUp(self):
		self._executor = BenchmarkHarnessCallableExecutor()

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

	# this is only going to work if the machine has at least two cores.
	def test_should_execute_callable_with_process_pinned_to_one_given_cpu_core(self):
		self.skipTest("can be added if/when this experiment is continued")
		def get_cpu_affinity() -> list[int]:
			return psutil.Process(os.getpid()).cpu_affinity()

		def target_callable():
			return get_cpu_affinity()
		self._executor.execute_callable()