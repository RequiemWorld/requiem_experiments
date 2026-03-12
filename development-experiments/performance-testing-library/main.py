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
