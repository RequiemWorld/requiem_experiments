from __future__ import annotations
import matplotlib


# This should probably not use timestamps, and probably shouldn't care about exact times
# probably just milliseconds/microseconds, and should use monotonic time to get it.
class ActionExecutionReport:
	def __init__(self,
				 timestamp_of_start: float,
				 timestamp_of_finish: float,
				 exception_encountered: Exception | None = None):
		self._timestamp_of_start = timestamp_of_start
		self._timestamp_of_finish = timestamp_of_finish
		self._exception_encountered = exception_encountered

	@property
	def exception(self) -> Exception | None:
		return self._exception_encountered

	@property
	def timestamp_of_start(self):
		return self._timestamp_of_start

	@property
	def timestamp_of_finish(self):
		return self._timestamp_of_finish

	@property
	def milliseconds_taken_to_execute(self) -> int:
		return int((self._timestamp_of_finish - self._timestamp_of_start) * 1000)

	def executed_without_exception(self) -> bool:
		return self._exception_encountered is None


class LoadExecutionReport:

	def __init__(self, action_execution_reports: list[ActionExecutionReport]):
		self._action_execution_report = action_execution_reports.copy()

	@property
	def action_execution_reports(self) -> list[ActionExecutionReport]:
		return self._action_execution_report
