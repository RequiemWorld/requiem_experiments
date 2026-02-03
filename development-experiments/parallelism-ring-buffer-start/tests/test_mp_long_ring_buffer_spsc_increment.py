import multiprocessing
import time
from dataclasses import dataclass
from experiment.ring_buffer import LongRingBuffer
from experiment.ring_buffer import IncrementWorker
from experiment.ring_buffer import IncrementHelper
from multiprocessing.shared_memory import SharedMemory


@dataclass
class Context:
	request_memory: SharedMemory
	response_memory: SharedMemory
	increment_helper: IncrementHelper
	process: multiprocessing.Process


def test_benchmark_incrementing_latency_with_long_ring_buffer(benchmark):

	context: Context | None = None
	def setup_context():
		nonlocal context
		request_memory = LongRingBuffer.make_shared_memory("experiments_request_memory", 0xFFFF)
		response_memory = LongRingBuffer.make_shared_memory("experiments_response_memory", 0xFFFF)
		request_buffer = LongRingBuffer(request_memory, capacity=0xFFFF)
		response_buffer = LongRingBuffer(request_memory, capacity=0xFFFF)
		increment_worker = IncrementWorker(request_buffer, response_buffer)
		increment_worker_process = multiprocessing.Process(target=increment_worker.execute)
		increment_worker_process.start()
		increment_helper = IncrementHelper(request_buffer, response_buffer)
		context = Context(request_memory, response_memory, increment_helper, increment_worker_process)

	def teardown_context():
		nonlocal context
		context.process.kill()
		context.request_memory.close()
		context.request_memory.unlink()
		context.response_memory.close()
		context.response_memory.unlink()
		context = None

	def benchmark_body():
		for _ in range(1000):
			context.increment_helper.increment_number(1)

	benchmark.pedantic(benchmark_body, setup=setup_context, teardown=teardown_context, rounds=5, iterations=1)
