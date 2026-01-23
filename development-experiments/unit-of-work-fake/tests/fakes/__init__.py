from fakedb import DatabaseTransaction
from fakedb import FakeDatabase
from experiment.entities import User
from experiment.entities import UserRepository
from experiment.entities import UnitOfWork


class FakeUserRepository(UserRepository):

    def __init__(self, transaction: DatabaseTransaction):
        self._transaction = transaction

    def add_new_user(self, user: User):
        self._transaction.add_new_entity(user)

    def find_by_id(self, id_: int) -> User:
        predicate = lambda user: user.id == id_
        return self._transaction.find_one_by_predicate(User, predicate)


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, fakedb: FakeDatabase):
        self._user_repo = FakeUserRepository(fakedb.new_transaction())

    @property
    def user_repo(self) -> UserRepository:
        return self._user_repo

    def commit(self):
        raise NotImplementedError