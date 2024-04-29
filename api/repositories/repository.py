from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    

    @abstractmethod
    async def create_user(cls):
        raise NotImplementedError
    
    @abstractmethod
    async def get_users(cls):
        raise NotImplementedError
    
    @abstractmethod
    async def acquire_lock(cls):
        raise NotImplementedError
    
    @abstractmethod
    async def release_lock(cls):
        raise NotImplementedError