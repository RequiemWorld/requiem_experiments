import pytest


def make_discord_snowflake(timestamp: int, worker: int, process: int, increment: int) -> int:
	"""
	Makes a discord snowflake with the given timestamp, worker, process and increment. Written
	in order of: increment (1-12), worker (13-17), process (18-23), timestamp (42).

	:param timestamp: The number of milliseconds since the epoch (42 bits) (officially 2015/01/01 00:00 UTC)
	:param worker: The worker number that is creating the snowflake (5 bits).
	:param process: The process number on the worker that is creating the snowflake (5 bits).
	:param increment: The increment for the timestamp (a maximum of 4095 can be generated per millisecond).

	:raises ValueError: When 'increment' is above 4095 or below 0.
	:raises ValueError: When 'worker' is above 31 or below 0.
	:raises ValueError: When 'process' is above 31 or below 0.
	:raises ValueError: When 'timestamp' is above 4398046511103 or below 0
	"""
	# ^^ The duplicate raises value error might not show up in IDE correctly,
	# and that will be something to sort out if this code is used in the future.
	if increment < 0:
		raise ValueError
	if increment > 4095:
		raise ValueError
	if worker < 0 or process < 0:
		raise ValueError
	if worker > 31 or process > 31:
		raise ValueError
	if timestamp < 0:
		raise ValueError
	if timestamp > 4398046511103:
		raise ValueError
	snowflake = increment
	snowflake |= worker << 12
	snowflake |= process << 17
	snowflake |= timestamp << 22
	return snowflake


class TestDiscordSnowflakeFunctionResultBits:

	@pytest.mark.parametrize("test_value", [0, 1, 4095])
	def test_should_have_given_increment_value_in_bits_1_to_12(self, test_value: int):
		snowflake = make_discord_snowflake(increment=test_value, worker=9, process=2, timestamp=2)
		assert snowflake & 4095 == test_value

	@pytest.mark.parametrize("test_value", [0, 1, 31])
	def test_should_have_given_internal_worker_value_in_bits_13_to_17(self, test_value: int):
		snowflake = make_discord_snowflake(increment=5, worker=test_value, process=2, timestamp=2)
		internal_worker = (snowflake >> 12) & 31
		assert internal_worker == test_value

	@pytest.mark.parametrize("test_value", [0, 1, 31])
	def test_should_have_given_internal_process_value_in_bits_18_to_22(self, test_value: int):
		snowflake = make_discord_snowflake(increment=5, worker=5, process=test_value, timestamp=2)
		internal_process = (snowflake >> 17) & 31
		assert internal_process == test_value

	@pytest.mark.parametrize("test_value", [0, 1, 4398046511103])
	def test_should_have_given_timestamp_value_in_bits_23_to_64(self, test_value):
		timestamp = make_discord_snowflake(increment=5, worker=5, process=0, timestamp=test_value)
		assert timestamp >> 22 == test_value


class TestDiscordSnowflakeFunctionInputErrors:

	def test_should_raise_ValueError_when_increment_above_4095(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=4096, worker=9, process=1, timestamp=2)

	def test_should_raise_ValueError_when_increment_below_0(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=-5, worker=9, process=1, timestamp=2)

	def test_should_raise_ValueError_when_worker_below_0(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=-3, process=1, timestamp=2)

	def test_should_raise_ValueError_when_worker_above_31(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=33, process=1, timestamp=2)

	def test_should_raise_ValueError_when_process_below_0(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=0, process=-2, timestamp=2)

	def test_should_raise_ValueError_when_process_above_31(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=0, process=33, timestamp=2)

	def test_should_raise_ValueError_when_timestamp_above_4398046511103(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=0, process=1, timestamp=4398046511109)

	def test_should_raise_ValueError_when_timestamp_below_0(self):
		with pytest.raises(ValueError):
			make_discord_snowflake(increment=1, worker=0, process=33, timestamp=-2)
	

def main() -> None:
	while True:
		comma_separated_input = input("enter values comma separated (worker, process, timestamp, increment): ")
		worker, process, timestamp, increment = comma_separated_input.split(",")
		worker, process, timestamp, increment = int(worker), int(process), int(timestamp), int(increment)
		snowflake_value = make_discord_snowflake(worker=worker, process=process, timestamp=timestamp, increment=increment)
		print(f"Snowflake has been made: {snowflake_value}")


if __name__ == "__main__":
	main()
