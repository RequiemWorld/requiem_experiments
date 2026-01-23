from . import FakeDatabaseTestCase
from . import NamedEntity
from . import IdAndNameEntity
from fakedb import DatabaseBackend

class TestBackendNewEntityMerging(FakeDatabaseTestCase):
    def setUp(self):
        super().setUp()
        self._database.backend.register_entity(NamedEntity, lambda entity: entity.name)

    def test_should_add_single_new_entity_via_merge_when_none_added_yet(self):
        find_john_predicate = lambda entity: entity.name == "John"
        entity = NamedEntity(name="John")
        self._database.backend.merge_entities([entity])
        found = self._database.backend.find_one_by_predicate(NamedEntity, find_john_predicate)
        self.assertEqual(found.name, "John")

    def test_should_add_multiple_new_entities_via_merge_when_none_added_yet(self):
        find_john_predicate = lambda entity: entity.name == "John"
        find_jane_predicate = lambda entity: entity.name == "Jane"
        john_entity = NamedEntity(name="John")
        jane_entity = NamedEntity(name="Jane")
        self._database.backend.merge_entities([john_entity, jane_entity])
        self.assertIsNotNone(self._database.backend.find_one_by_predicate(NamedEntity, find_john_predicate))
        self.assertIsNotNone(self._database.backend.find_one_by_predicate(NamedEntity, find_jane_predicate))


class TestBackendEntityUpdateMerging(FakeDatabaseTestCase):
    def setUp(self):
        super().setUp()
        self._database.backend.register_entity(NamedEntity, lambda entity: entity.name)
        self._database.backend.register_entity(IdAndNameEntity, lambda entity: entity.id)

    def test_should_add_new_entity_instead_of_modifying_old_when_identifier_has_changed(self):
        john_entity = NamedEntity(name="John")
        john_changed_to_joe_entity = NamedEntity(name="Joe")
        find_john_predicate = lambda entity: entity.name == "John"
        find_joe_predicate = lambda entity: entity.name == "Joe"
        self._database.backend.add_new_entities([john_entity])
        self._database.backend.merge_entities([john_changed_to_joe_entity])
        self.assertIsNotNone(self._database.backend.find_one_by_predicate(NamedEntity, find_john_predicate))
        found_joe_entity = self._database.backend.find_one_by_predicate(NamedEntity, find_joe_predicate)
        self.assertEqual(found_joe_entity.name, "Joe")

    def test_should_effectively_update_attributes_of_entity_when_modified_and_merging(self):
        joe_entity_original = IdAndNameEntity(id_="1", name="Joe")
        joe_entity_modified = IdAndNameEntity(id_="1", name="John")
        self._database.backend.add_new_entities([joe_entity_original])
        self._database.backend.merge_entities([joe_entity_modified])
        found_joe = self._database.backend.find_one_by_predicate(IdAndNameEntity, lambda entity: entity.id == "1")
        self.assertEqual(found_joe.name, "John")

