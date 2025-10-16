from datetime import datetime
from datetime import timezone


DISCORD_EPOCH = datetime(year=2015, month=1, day=1, tzinfo=timezone.utc)
def read_snowflake_timestamp(snowflake: int) -> int:
	"""
	Returns the stored number of milliseconds since 2015/01/01 00:00 UTC.
	"""
	timestamp_number = snowflake >> 22
	return timestamp_number


def read_snowflake_increment(snowflake: int) -> int:
	return snowflake & 4095


def read_snowflake_internal_worker_and_process_id(snowflake: int) -> tuple[int, int]:
	# bits 13-17 are the internal worker id
	internal_worker_id = (snowflake >> 12) & 31
	# bits 18-22 are the internal process id
	internal_process_id = (snowflake >> 17) & 31
	return internal_worker_id, internal_process_id


def read_datetime_from_millisecond_timestamp(timestamp: int) -> datetime:
	"""
	:param timestamp: the amount of milliseconds since 2015/01/01 00:00 UTC.
	"""
	epoch_timestamp: float = DISCORD_EPOCH.timestamp()
	adjusted_to_normal: float = epoch_timestamp + (timestamp / 1000)
	return datetime.fromtimestamp(adjusted_to_normal, tz=timezone.utc)

def main() -> None:
	while True:
		snowflake_input = int(input("Enter discord snowflake to read: "))
		millisecond_timestamp = read_snowflake_timestamp(snowflake_input)
		internal_worker_id, internal_process_id = read_snowflake_internal_worker_and_process_id(snowflake_input)
		increment = read_snowflake_increment(snowflake_input)
		print("-" * 10)
		print("decoded internal worker:", internal_worker_id)
		print("decoded internal process:", internal_process_id)
		print("decoded increment:", increment)
		print("decoded timestamp date:", read_datetime_from_millisecond_timestamp(millisecond_timestamp), "(utc)")
		print("-" * 10)

if __name__ == "__main__":
	main()