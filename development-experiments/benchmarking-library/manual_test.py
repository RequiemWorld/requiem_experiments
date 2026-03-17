import time
from speedtest import CallableSpeedTester
from speedtest import CallableBenchmarker


benchmarker = CallableBenchmarker(CallableSpeedTester(time.time_ns))
benchmark_result = benchmarker.benchmark_callable(lambda: time.sleep(0), iterations=1000000)
print(benchmark_result.to_presentable_result())