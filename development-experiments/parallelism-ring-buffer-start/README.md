## Purpose of Experiment

The purpose of this experiment was to get started with interprocess communication in general and in python with multiprocessing, having a worker on (assuming scheduled right) another CPU core. The default approach is to use a queue between the processes which is not efficient for our purposes.

- We need to send messages to other threads or processes to get work done and receive responses back. A queue was the simplest option even if not desired and allowed for comparing it against a ring buffer solution.
- The experiment involved having a worker own a sequence and take requests to increment it and report back the current state.
  - I'm not aware of the internal workings of the multiprocessing.Queue class. The problem can be optimized with a single producer/single consumer ring buffer.


I'm keeping some of the research and planning for this internal to the project. A very simple ring buffer for ints as longs has been written and shared memory been used. This was an experiment to get hands on with both of those things, and as expected, the ring buffer performs faster.

## Performance Results

A simple benchmark was written which spawn a process and use a helper class to send requests to increment the number and read a response 1000 times in one go. I'm sure this benchmark is not too proper but the stark difference in results should say something. Benchmarks will get better on the project with time. See: ``tests/test_mp_long_ring_buffer_spsc_increment.py``, and ``tests/test_mp_queue_spsc_increment.py``

- [multiprocessing.Queue VS our ring buffer for longs](https://ibb.co/NbZSCnS) : Python3.13
- [multiprocessing.Queue VS our ring buffer for longs](https://ibb.co/KjqCCHfb) : pypy3.11
