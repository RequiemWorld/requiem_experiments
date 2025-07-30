from __future__ import annotations
import abc
import random
import asyncio
from typing import Callable


class IterationWaitStrategy:

	@abc.abstractmethod
	async def wait(self):
		raise NotImplementedError


class BetweenSecondsIterationWaitStrategy(IterationWaitStrategy):
	def __init__(self, between_x: float, between_y: float):
		self._between_x = between_x
		self._between_y = between_y

	def _get_random_wait_time_between_x_and_y(self):
		wait_time = random.uniform(self._between_x, self._between_y)
		return wait_time

	async def wait(self):
		random_wait_time = self._get_random_wait_time_between_x_and_y()
		await asyncio.sleep(random_wait_time)


class VirtualUser(abc.ABC):

	@abc.abstractmethod
	async def dispose(self):
		raise NotImplementedError

	@abc.abstractmethod
	async def execute(self):
		raise NotImplementedError


class SharedVirtualUserContext:
	def __init__(self, active_virtual_user_count: int):
		self.active_virtual_user_count = active_virtual_user_count


class InfiniteVirtualUser(VirtualUser):
	"""
	A virtual user that will go infinitely until disposed of.
	"""
	def __init__(self, coroutine_factory, wait_strategy: IterationWaitStrategy):
		self._coroutine_factory = coroutine_factory
		self._wait_strategy = wait_strategy
		self._execution_finished_event = asyncio.Event()
		self._has_execute_been_called = False
		self._has_dispose_been_called = False

	async def dispose(self):
		self._has_dispose_been_called = True
		await self._execution_finished_event.wait()

	async def execute(self):
		self._has_execute_been_called = True
		while not self._has_dispose_been_called:
			await self._wait_strategy.wait()
		self._execution_finished_event.set()


class VirtualUserManager:
	def __init__(self, virtual_user_factory: Callable[[], VirtualUser]):
		self._virtual_user_factory = virtual_user_factory
		self._virtual_users: list[VirtualUser] = list()

	async def spawn_virtual_user(self):
		raise NotImplementedError

	async def cleanup_virtual_users(self):
		raise NotImplementedError
