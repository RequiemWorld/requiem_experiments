import multiprocessing
from dataclasses import dataclass
from experiment.queue import IncrementWorker, IncrementHelper

@dataclass
class Context:
	increment_helper: IncrementHelper
	process: multiprocessing.Process


def test_benchmark_incrementing_latency_with_queue(benchmark):

	context: Context | None = None
	def setup_context():
		nonlocal context
		request_queue = multiprocessing.Queue()
		response_queue = multiprocessing.Queue()
		increment_worker = IncrementWorker(request_queue, response_queue)
		increment_worker_process = multiprocessing.Process(target=increment_worker.execute)
		increment_worker_process.start()
		increment_helper = IncrementHelper(request_queue, response_queue)
		context = Context(increment_helper, increment_worker_process)

	def teardown_context():
		nonlocal context
		context.process.kill()
		context = None

	def benchmark_body():
		for _ in range(1000):
			context.increment_helper.increment_number(1)

	benchmark.pedantic(benchmark_body, setup=setup_context, teardown=teardown_context, rounds=5, iterations=1)
