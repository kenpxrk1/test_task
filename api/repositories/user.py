import datetime
from typing import List
from uuid import UUID
from fastapi import Depends
from sqlalchemy import insert, select, text, update
from api.models import UserModel
from api.db import async_session
from .repository import AbstractRepository
from api.schemas import UserСreateDTO, UserReadDTO
from api.exc import UserAlreadyLockedError
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(AbstractRepository):

    """ 
    Class UserRepository is using for incapsulated work
    with database by SQLAlchemy orm, inherited from AbstractRepository
    """

    @classmethod
    async def create_user(cls, data: dict, session: AsyncSession) -> UserReadDTO:
        """
        create_user realize classmethod that adding new user
        into a database, takings dictionary parameter with user
        data and returns nothing.
        """
        created_user = (
            insert(UserModel).values(**data).returning(UserModel)
        )
        user = await session.execute(created_user)
        await session.commit()
        user = user.scalar_one()
        return UserReadDTO.model_validate(user, from_attributes=True)
        

    @classmethod
    async def get_users(cls, session: AsyncSession) -> List[UserReadDTO | None]:
        """
        get_users realize classmethod that returns a list
        of UserDTO objects 
        """
        
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
    async def set_locktime(cls, id: UUID, session: AsyncSession) -> UserReadDTO:
        """
        set_locktime takes id param and setting locktime 
        for user by his id. Returns UserReadDTO object 
        or None if user does not exist.
        """
        user = await session.get(UserModel, id)
        if user == None:
            raise TypeError
        if user.locktime != None:
            raise UserAlreadyLockedError
        user.locktime = datetime.datetime.now()
        await session.commit()
        return UserReadDTO.model_validate(user, from_attributes=True)



    @classmethod
    async def reset_locktime(cls, id: UUID, session: AsyncSession) -> UserReadDTO:
        """ 
        reset_locktime takes id param and 
        resetting locktime for user. Returns UserReadDTO object.
        """
        user = await session.get(UserModel, id)
        if user == None:
            raise TypeError
        user.locktime = None
        await session.commit()
        return UserReadDTO.model_validate(user, from_attributes=True)