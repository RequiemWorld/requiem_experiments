import unittest
from perftooling.generation import calculate_ramp_up_sleep_interval


class TestRampUpSleepIntervalCalculationFunctionErrors(unittest.TestCase):

	def test_should_raise_value_error_when_the_target_users_is_zero(self):
		with self.assertRaises(ValueError):
			calculate_ramp_up_sleep_interval(0, 10)

	def test_should_raise_value_error_when_the_target_users_is_negative(self):
		with self.assertRaises(ValueError):
			calculate_ramp_up_sleep_interval(-8, 10)

	def test_should_raise_value_error_when_ramp_up_seconds_is_zero(self):
		with self.assertRaises(ValueError):
			calculate_ramp_up_sleep_interval(10, 0)

	def test_should_raise_value_error_when_ramp_up_seconds_is_negative(self):
		with self.assertRaises(ValueError):
			calculate_ramp_up_sleep_interval(10, -5)



class TestRampUpSleepIntervalCalculationSimpleMath(unittest.TestCase):
	def test_should_return_value_with_precision_as_expected(self):
		# 7 / 300 (0.023333333333333334) (ramp up to 300 in 7 seconds)
		calculation = calculate_ramp_up_sleep_interval(300, 7)
		self.assertEqual(0.023333333333333334, calculation)

	def test_should_return_right_sleep_interval_with_value_of_100_as_should_make_sense_01(self):
		# 100 users in 10 seconds, would require spawning one every 0.1 seconds i.e. 10 seconds divided by 100 (0.1)
		calculation = calculate_ramp_up_sleep_interval(100, 10)
		self.assertEqual(0.1, calculation)

	def test_should_return_right_sleep_interval_with_value_of_100_as_should_make_sense_02(self):
		# 60 / 100 (0.6) (sleep 0.6 seconds to spawn all users in within
		calculation = calculate_ramp_up_sleep_interval(100, 60)
		self.assertEqual(0.6, calculation)