import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from .enums import UserDomain


class UserBaseDTO(BaseModel):
    login: EmailStr


class UserСreateDTO(UserBaseDTO):
    password: str
    project_id: UUID
    domain: UserDomain


class UserReadDTO(UserBaseDTO):
    id: UUID
    created_at: datetime.datetime
    project_id: UUID
    env: str
    domain: UserDomain
    locktime: datetime.datetime | None


# class AcquireLockRequest:
#     id: UUID
