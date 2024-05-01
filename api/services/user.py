from typing import List
from uuid import UUID
from api.repositories.user import UserRepository
from api.schemas import UserReadDTO, UserСreateDTO
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(
        self, request: UserСreateDTO, session: AsyncSession
    ) -> UserReadDTO:
        """
        create_user taking in params a request with UserCreateDTO object,
        deserialize it into a dict object, hashing password from request
        and sends new object to database logic. returns UserReadDTOP

        """
        request_dict = request.model_dump()
        request_dict["password"] = bcrypt_context.hash(request_dict["password"])
        user = await self.repository.create_user(request_dict, session)
        return user

    async def get_users(self, session: AsyncSession) -> List[UserReadDTO | None]:
        """
        calling a self repository get_users method and returns
        list of UserReadDTO objects or None.
        """
        users = await self.repository.get_users(session)
        return users

    async def acquire_lock(self, id: UUID, session: AsyncSession) -> UserReadDTO:
        """
        calling a self repository set_locktime method and returns
        UserReadDTO object.
        """
        user = await self.repository.set_locktime(id, session)
        return user

    async def release_lock(self, id: UUID, session: AsyncSession) -> UserReadDTO:
        """
        calling a self repository release_lock method and returns
        UserReadDTO object.
        """
        user = await self.repository.reset_locktime(id, session)
        return user
