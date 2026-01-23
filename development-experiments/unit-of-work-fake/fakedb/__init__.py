import abc
import copy
from typing import Any
from typing import Type
from typing import Callable


Entity = Type
EntityInstance = object
Predicate = Callable[[Entity], bool]
Identify = Callable[[Entity], Any]
def copy_entity(entity: Entity) -> Entity:
    return copy.deepcopy(entity)


# When iterating through a list
class StoredEntity:
    def __init__(self, entity: EntityInstance) -> None:
        self.entity = entity

class DatabaseBackend:
    def __init__(self):
        self._stored_entities: list[StoredEntity] = list()
        self._entities_to_identify_callables: dict[Entity, Identify] = dict()

    def register_entity(self, entity: Entity, identify: Identify) -> None:
        self._entities_to_identify_callables[entity] = identify

    def _identify_entity(self, entity: EntityInstance) -> Any:
        # TODO maybe add memoization or something here
        return self._entities_to_identify_callables[type(entity)](entity)

    def _check_for_entity(self, entity: EntityInstance) -> bool:
        """
        Checks if an entity of that type exists with the id that can be resolved for it.
        """
        given_entity_id = self._identify_entity(entity)
        for stored_entity in self._stored_entities:
            if self._identify_entity(stored_entity.entity) == given_entity_id:
                return True
        return False

    def merge_entities(self, entities: list[Entity]) -> None:
        """
        Merges a list of entities into existing ones, replacing
        ones held within, with the new ones and their updated values.
        """
        for merge_entity in entities:
            if not self._check_for_entity(merge_entity):
                self._stored_entities.append(StoredEntity(copy_entity(merge_entity)))
            merge_entity_type = type(merge_entity)
            merge_entity_id = self._identify_entity(merge_entity)
            for stored_entity in self._stored_entities:
                stored_entity_type = type(stored_entity.entity)
                stored_entity_id = self._identify_entity(stored_entity.entity)
                if stored_entity_type == merge_entity_type and stored_entity_id == merge_entity_id:
                   stored_entity.entity = merge_entity

    def add_new_entities(self, entities: list[object]):
        for entity in entities:
            self._stored_entities.append(StoredEntity(copy.deepcopy(entity)))

    def find_one_by_predicate(self, type_: Type, predicate: Predicate) -> Entity | None:
        """
        Finds an entity in the database and returns a copy.
        """
        for stored_entity in self._stored_entities:
            if type(stored_entity.entity) == type_:
                if predicate(stored_entity.entity):
                    return copy_entity(stored_entity.entity)
        return None


class DatabaseTransaction:
    def __init__(self, backend: DatabaseBackend):
        self._pending_entities = list()
        self._backend = backend

    def add_new_entity(self, entity: object) -> None:
        self._pending_entities.append(entity)

    def find_one_by_predicate(self, type_: Type, predicate: Predicate) -> Entity | None:
        for entity in self._pending_entities:
            if type(entity) == type_:
                if predicate(entity):
                    return entity
        found_entity = self._backend.find_one_by_predicate(type_, predicate)
        self._pending_entities.append(found_entity)
        return found_entity

    def commit(self) -> None:
        self._backend.merge_entities(self._pending_entities)

    def rollback(self) -> None:
        raise NotImplementedError


class FakeDatabase:
    def __init__(self):
        self._backend = DatabaseBackend()

    @property
    def backend(self):
        return self._backend

    def new_transaction(self) -> DatabaseTransaction:
        return DatabaseTransaction(self._backend)

