

def calculate_ramp_up_sleep_interval(target_users: int, ramp_up_seconds: int) -> float:
	"""
	When there is a need to gradually increase the number of users to the target amount over time,
	the idea is to sleep between each spawning of a user and this is the calculation of the amount to sleep by.

	:raises ValueError: When target_users is 0 or less than ramp up seconds, or when ramp_up_seconds is below or equal to 0.
	"""
	if target_users <= 0 or ramp_up_seconds <= 0:
		raise ValueError

	return ramp_up_seconds / target_users