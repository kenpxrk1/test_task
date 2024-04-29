import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from .enums import Domain

class UserBaseDTO(BaseModel):
    login: EmailStr

class UserСreateDTO(UserBaseDTO):
    password: str
    project_id: UUID
    domain: Domain
    
class UserReadDTO(UserBaseDTO):
    id: UUID 
    created_at: datetime.datetime
    project_id: UUID
    env: str
    domain: Domain
    locktime: datetime.datetime | None

