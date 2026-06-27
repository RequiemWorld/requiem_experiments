import asyncio
from asyncio import StreamReader
from asyncio import StreamWriter
from asyncio import start_unix_server
from datetime import datetime
from shared_communication import recv_datetime
from shared_communication import send_datetime


class ListeningClient:
	def __init__(self, writer: StreamWriter):
		self.is_active = True
		self._writer = writer

	async def publish_unix_date(self, date: datetime) -> None:
		print(f"[listening client] publishing {date}")
		await send_datetime(self._writer, date)


class BroadcastContext:
	def __init__(self):
		self._clients: set[ListeningClient] = set()

	def register_client(self, client: ListeningClient):
		self._clients.add(client)

	def deregister_client(self, client: ListeningClient):
		self._clients.remove(client)

	async def publish_unix_date(self, date: datetime) -> None:
		for client in self._clients:
			await client.publish_unix_date(date)

async def _wait_for_connection_to_end(stream_reader: StreamReader) -> None:
	while True:
		data = await stream_reader.read(1)
		if data == b"":
			break

async def main() -> None:
	import sys
	desired_socket_path = sys.argv[1]
	broadcast_context = BroadcastContext()
	async def handle_connection_lifecycle(reader: StreamReader, writer: StreamWriter):
		print("accepted connection")
		our_client = ListeningClient(writer)
		broadcast_context.register_client(our_client)
		try:
			print("waiting for connection to end")
			await _wait_for_connection_to_end(reader)
		finally:
			broadcast_context.deregister_client(our_client)

	async def continuously_publish_date() -> None:
		print("trying to broadcast date")
		while True:

			await broadcast_context.publish_unix_date(datetime.now())
			await asyncio.sleep(1)

	unix_server = await start_unix_server(handle_connection_lifecycle, path=desired_socket_path)
	asyncio.get_running_loop().create_task(continuously_publish_date())
	await unix_server.serve_forever()


if __name__ == "__main__":
	asyncio.run(main())