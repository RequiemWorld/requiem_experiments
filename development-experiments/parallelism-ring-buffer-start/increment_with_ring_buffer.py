import multiprocessing
from experiment.ring_buffer import LongRingBuffer, IncrementWorker, IncrementHelper


def main() -> None:
	request_memory = LongRingBuffer.make_shared_memory("experiments_request_memory", 0xFFFF)
	response_memory = LongRingBuffer.make_shared_memory("experiments_response_memory", 0xFFFF)
	request_buffer = LongRingBuffer(request_memory, capacity=0xFFFF)
	response_buffer = LongRingBuffer(request_memory, capacity=0xFFFF)
	increment_worker = IncrementWorker(request_buffer, response_buffer)
	increment_worker_process = multiprocessing.Process(target=increment_worker.execute)
	increment_worker_process.start()
	increment_helper = IncrementHelper(request_buffer, response_buffer)
	print(increment_helper.increment_number(50))
	print(increment_helper.increment_number(60))
	print(increment_helper.increment_number(60))

	request_memory.close()
	request_memory.unlink()
	response_memory.close()
	response_memory.unlink()


if __name__ == '__main__':
	main()
