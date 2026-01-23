import unittest
from . import FakeDatabaseTestCase, NamedEntity


class TestUpdatingEntityOnlyInTransaction(FakeDatabaseTestCase):
    def test_should_not_change_original_entity_when_modifying_one_from_transaction_without_commiting(self):
        self._database.backend.register_entity(NamedEntity, lambda named: named.name == "Joe")
        find_joe_predicate = lambda entity: entity.name == "Joe"
        transaction = self._database.new_transaction()
        transaction.add_new_entity(NamedEntity("Joe"))
        transaction.commit()

        transaction = self._database.new_transaction()
        entity = transaction.find_one_by_predicate(NamedEntity, find_joe_predicate)
        entity.name = "John"
        found = self._database.backend.find_one_by_predicate(NamedEntity, find_joe_predicate)
        self.assertIsNotNone(found, "joe should be findable in the database still")
        self.assertEqual(found.name, "Joe")


class TestOriginalEntityUpdatingAfter(FakeDatabaseTestCase):
    def test_should_modify_stored_entity_after_updating_in_transaction_and_commiting(self):
        find_joe_predicate = lambda entity: entity.name == "Joe"
        find_john_predicate = lambda entity: entity.name == "John"
        self._database.backend.register_entity(NamedEntity, lambda named: named.name == "Joe")
        transaction = self._database.new_transaction()
        transaction.add_new_entity(NamedEntity("Joe"))
        transaction.commit()
        transaction = self._database.new_transaction()
        entity = transaction.find_one_by_predicate(NamedEntity, find_joe_predicate)
        entity.name = "John"
        transaction.commit()

        # found_joe = self._database.backend.find_one_by_predicate(NamedEntity, find_joe_predicate)
        # self.assertIsNone(found_joe)
        found_john = self._database.backend.find_one_by_predicate(NamedEntity, find_john_predicate)
        self.assertEqual(found_john.name, "John")
