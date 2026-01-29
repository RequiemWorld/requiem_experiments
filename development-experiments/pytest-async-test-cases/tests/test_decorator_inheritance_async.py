import pytest


# https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_class_tests_in_same_loop.html
@pytest.mark.asyncio(loop_scope="class")
class MyCustomTestCase:
	pass


class TestAnotherThing(MyCustomTestCase):

	async def test_should_do_something_else(self):
		pytest.fail()

	async def test_should_do_another_thing(self):
		pass