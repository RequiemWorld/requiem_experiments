from speedtest import LoadRunner
from tests import LoadRunnerTestFixture


class TestLoadRunnerResultInformation(LoadRunnerTestFixture):
    async def test_should_have_amount_of_times_target_executed_on_result(self):
        self._load_runner.arrival_rate = 20
        self._load_runner.run_duration = 1
        result = await self._load_runner.execute()
        self.assertEqual(20, result.execution_count)


class TestLoadRunnerArrivalRate(LoadRunnerTestFixture):
    async def test_should_execute_one_time_for_arrival_1_and_duration_1(self):
        self._load_runner.arrival_rate = 1
        self._load_runner.run_duration = 1
        await self._load_runner.execute()
        self.assertEqual(1, self._dummy_target_execution_count)

    async def test_should_execute_two_times_for_arrival_2_and_duration_1(self):
        self._load_runner.arrival_rate = 2
        self._load_runner.run_duration = 1
        await self._load_runner.execute()
        self.assertEqual(2, self._dummy_target_execution_count)

    async def test_should_execute_four_times_for_arrival_2_and_duration_2(self):
        self._load_runner.arrival_rate = 2
        self._load_runner.run_duration = 2
        await self._load_runner.execute()
        self.assertEqual(4, self._dummy_target_execution_count)

    async def test_should_execute_1000_times_for_arrival_100_and_duration_10(self):
        self._load_runner.arrival_rate = 100
        self._load_runner.run_duration = 10
        await self._load_runner.execute()
        self.assertEqual(1000, self._dummy_target_execution_count)


class TestLoadRunnerPerformance(LoadRunnerTestFixture):

    async def test_should_be_able_to_execute_target_25000_times_in_one_second(self):
        self._load_runner.run_duration = 1
        self._load_runner.arrival_rate = 25000
        load_runner_result = await self._load_runner.execute()
        speed_test_results = load_runner_result.speed_test_results
        self.assertEqual(25000, self._dummy_target_execution_count)
        self.assertAllResultsExecutedWithinOneSecond(speed_test_results)


class TestLoadRunnerErrors(LoadRunnerTestFixture):

    async def test_should_return_result_with_error_count_of_1_on_only_execution_done(self):
        self._load_runner.arrival_rate = 1
        self._load_runner.run_duration = 1
        self._dummy_target_error_to_raise = Exception
        result = await self._load_runner.execute()
        self.assertEqual(1, result.error_count)
