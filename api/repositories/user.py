from typing import List
from fastapi import Depends
from sqlalchemy import insert, select
from api.models import UserModel
from api.db import async_session
from .repository import AbstractRepository
from api.schemas import UserСreateDTO, UserReadDTO
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(AbstractRepository):

    """ 
    Class UserRepository is using for incapsulated work
    with database by SQLAlchemy orm, inherited from AbstractRepository
    """

    @classmethod
    async def create_user(cls, data: dict) -> None:
        """
        create_user realize classmethod that adding new user
        into a database, takings dictionary parameter with user
        data and returns nothing.
        """
        async with async_session() as session:
            created_user = (
                insert(UserModel).values(**data)
            )
            await session.execute(created_user)
            await session.commit()


    @classmethod
    async def get_users(cls) -> List[UserReadDTO | None]:
        """
        get_users realize classmethod that returns a list
        of UserDTO objects 
        """
        async with async_session() as session:
            users_query = (
                select(UserModel)
            )
            users = await session.execute(users_query)
            users = users.scalars().all()
            if users == None:
                return []
                
            return [
                UserReadDTO.model_validate(user, from_attributes=True) for user in users
            ]

    @classmethod
    async def acquire_lock(cls):
        ...

    @classmethod
    async def release_lock(cls):
        return 1
