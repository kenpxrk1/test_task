import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from .enums import UserDomainEnum, EnvModeEnum


class UserBaseDTO(BaseModel):
    login: EmailStr


class UserСreateDTO(UserBaseDTO):
    password: str
    project_id: UUID
    domain: UserDomainEnum


class UserReadDTO(UserBaseDTO):
    id: UUID
    created_at: datetime.datetime
    project_id: UUID
    env: EnvModeEnum
    domain: UserDomainEnum
    locktime: datetime.datetime | None



