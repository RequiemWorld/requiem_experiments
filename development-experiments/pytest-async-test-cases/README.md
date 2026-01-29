## Discovery 1  - async functions/methods aren't natively supported

- pytest will error and say that async def functions aren't natively supported when you write a test class and add an async test method and try to run it. [\[1\]](https://ibb.co/G39KPc60)

## Discovery 2 -> async functions/methods supported by marker through pytest-asyncio
- pytest can use async functions/methods decorated with the ``pytest.mark.asyncio`` marker. By default, each async test must be decorated with it. This can be remedied on classes by decorating the class with the marker. [\[1\]](https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_class_tests_in_same_loop.html)
- inheritance support: a base test case class can be made and the async methods on the child classes will run without decorators. [\[1\]](https://ibb.co/xtxKdfrw)