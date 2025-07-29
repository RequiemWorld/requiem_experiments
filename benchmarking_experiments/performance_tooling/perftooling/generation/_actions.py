from __future__ import annotations
from typing import Awaitable, Callable


class Action:
	def __init__(self, awaitable: Awaitable, time_provider: Callable[[], float]):
		self._awaitable = awaitable
		self._time_provider = time_provider
		self._time_execution_started: float | None = None
		self._time_execution_finished: float | None = None
		self._has_executed_and_completed = False

	@property
	def has_executed_and_completed(self) -> bool:
		return self._has_executed_and_completed

	@property
	def execution_time_in_milliseconds(self) -> int | None:
		"""
		Returns the amount of time it took to execute in milliseconds, e.g. 200ms.
		"""

		if self._time_execution_started is None or self._time_execution_finished is None:
			return None
		return int((self._time_execution_finished - self._time_execution_started) * 1000)

	async def execute(self):
		self._time_execution_started = self._time_provider()
		await self._awaitable
		self._time_execution_finished = self._time_provider()
		self._has_executed_and_completed = True
