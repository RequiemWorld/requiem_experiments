import unittest
from fakedb import DatabaseBackend
from fakedb import FakeDatabase


class FakeDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self._database = FakeDatabase()


class NamedEntity:
    def __init__(self, name: str):
        self.name = name

class IdAndNameEntity:
    def __init__(self, id_: str, name: str):
        self.id = id_
        self.name = name
