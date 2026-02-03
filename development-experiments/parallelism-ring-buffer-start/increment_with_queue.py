import multiprocessing
from experiment.queue import IncrementWorker, IncrementHelper


def main() -> None:
	request_queue = multiprocessing.Queue()
	response_queue = multiprocessing.Queue()
	increment_worker = IncrementWorker(request_queue, response_queue)
	increment_worker_process = multiprocessing.Process(target=increment_worker.execute)
	increment_worker_process.start()
	increment_helper = IncrementHelper(request_queue, response_queue)
	print(increment_helper.increment_number(50))
	print(increment_helper.increment_number(60))
	print(increment_helper.increment_number(60))


if __name__ == "__main__":
	main()