from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def create_user():
        raise NotImplementedError

    @abstractmethod
    async def get_users():
        raise NotImplementedError

    @abstractmethod
    async def set_locktime():
        raise NotImplementedError

    @abstractmethod
    async def reset_locktime():
        raise NotImplementedError
