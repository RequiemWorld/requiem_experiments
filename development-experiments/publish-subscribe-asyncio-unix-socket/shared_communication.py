from asyncio import StreamReader
from asyncio import StreamWriter
from datetime import datetime


def _serialize_datetime(date: datetime) -> bytes:
	return int(date.timestamp()).to_bytes(4, "big", signed=False)

def _deserialize_datetime(data: bytes) -> datetime:
	return datetime.fromtimestamp(int.from_bytes(data, "big", signed=False))


async def send_datetime(writer: StreamWriter, date: datetime) -> bytes:
	writer.write(_serialize_datetime(date))
	await writer.drain()


async def recv_datetime(reader: StreamReader) -> datetime:
	timestamp_bytes = await reader.read(4)
	if timestamp_bytes == b"":
		raise EOFError
	return _deserialize_datetime(timestamp_bytes)