# Purpose of Experiment
Write a performance testing library to take any asyncio code and measure the speed of the system under test is. Our automated testing infrastructure for stuff that allows for interacting with the system and using various features is already written as part of our acceptance testing effort and it is done for convenience in asyncio which is not aligned with the concurrency approach of the only existing performance testing library, locust. 


## Coordinated Omission

This is intended address the coordinated omission problem by borrowing the arrival rate usage available in k6. The target async code will be called at the **arrival_rate** every second for the given **run_duration**, it will not back off of the system by waiting for the old ones to complete before starting the batch of new ones.

## Example Usage/Result
```python
import httpx
import asyncio
from speedtest import LoadRunner
from speedtest.display import print_load_run_result


# constructing this seems to take hundreds of milliseconds
client = httpx.AsyncClient()


async def _request_bing_dot_com():
    await client.get("http://bing.com/index.html")


async def main() -> None:
    load_runner = LoadRunner(target=_request_bing_dot_com)
    load_runner.arrival_rate = 1  # how many per second
    load_runner.run_duration = 10  # how many seconds to run for
    load_run_result = await load_runner.execute()
    print_load_run_result(load_run_result)
    assert load_run_result.percentile_99_9999 < 500, f"tail latency should be less than 500ms, got {load_run_result.percentile_99_9999}"


asyncio.run(main())
```

```
+--------------+----------+-----------+-----------+------------+
|   executions |   errors |   minimum |   maximum |   p99.9999 |
+==============+==========+===========+===========+============+
|           10 |        0 |        20 |       115 |    115.894 |
+--------------+----------+-----------+-----------+------------+
```