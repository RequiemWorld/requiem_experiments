import unittest
from dataclasses import dataclass


@dataclass
class PerformanceTestSettings:
    arrival_rate: int
    run_duration: int
    acceptable_error_count: int = 0
    acceptable_maximum_latency: int = 0
    acceptable_minimum_latency: int = 0


def _tag_target_with_goals(target, goals: PerformanceTestSettings):
    target.goals = goals


def _read_goals_from_target(target) -> PerformanceTestSettings:
    assert hasattr(target, "goals")
    return target.goals


class PerformanceTestCase(unittest.IsolatedAsyncioTestCase):
    def __init_subclass__(cls, **kwargs):
        raise NotImplementedError
