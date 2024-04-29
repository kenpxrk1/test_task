import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func, text
from .enums import Domain
from .config import settings

class Base(DeclarativeBase):
    pass 

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    project_id: Mapped[UUID]
    env: Mapped[str] = mapped_column(server_default=settings.ENV_MODE)
    domain: Mapped[Domain]
    locktime: Mapped[datetime.datetime] = mapped_column(nullable=True)