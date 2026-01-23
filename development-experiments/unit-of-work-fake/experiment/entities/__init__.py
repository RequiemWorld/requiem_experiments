import abc


class Party:
    def __init__(self, id_: int, name: str):
        self.id_ = id_
        self.name = name


class User:
    def __init__(self, id_: int, username: str, currency_1_amount: int, currency_2_amount: int):
        self.id_ = id_
        self.username = username
        self.currency_1_amount = currency_1_amount
        self.currency_2_amount = currency_2_amount


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add_new_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, id_: int) -> User:
        raise NotImplementedError

class UnitOfWork(abc.ABC):

    @property
    @abc.abstractmethod
    def user_repo(self) -> UserRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

