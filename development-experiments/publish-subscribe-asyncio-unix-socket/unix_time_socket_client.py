import sys
import asyncio
from asyncio import StreamReader
from shared_communication import recv_datetime


async def _time_printing_loop(reader: StreamReader):
	while True:
		print("trying to read")
		try:
			date = await recv_datetime(reader)
		except EOFError:
			print("end of file")
			return
		print(date)


async def main() -> None:
	unix_socket_path = sys.argv[1]
	reader, _ = await asyncio.open_unix_connection(path=unix_socket_path)
	await _time_printing_loop(reader)

if __name__ == '__main__':
	asyncio.run(main())