import unittest
from fakedb import FakeDatabase
from . import FakeDatabaseTestCase
from . import NamedEntity

class TestEntityCreateTransaction(FakeDatabaseTestCase):

    def test_should_place_entity_in_backend_after_commit(self):
        self._database.backend.register_entity(NamedEntity, lambda entity: entity.name)
        transaction = self._database.new_transaction()
        transaction.add_new_entity(NamedEntity("Joe"))
        transaction.commit()
        found = self._database.backend.find_one_by_predicate(NamedEntity, lambda entity: entity.name == "Joe")
        self.assertEqual("Joe", found.name)

    def test_should_not_place_entity_in_backend_before_commit(self):
        self._database.backend.register_entity(NamedEntity, lambda entity: entity.name)
        transaction = self._database.new_transaction()
        transaction.add_new_entity(NamedEntity("Joe"))
        joe_entity = self._database.backend.find_one_by_predicate(NamedEntity, lambda entity: entity.name == "Joe")
        self.assertIsNone(joe_entity)