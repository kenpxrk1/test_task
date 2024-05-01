import datetime
from typing import AsyncGenerator
from uuid import UUID
import asyncpg
from pydantic import EmailStr
from api.db import get_async_session
from api.enums import UserDomain
from api.main import app
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio
import pytest
from api.config import settings
from api.models import Base

async_engine = create_async_engine(settings.TEST_DATABASE_URL)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_init(event_loop):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with async_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def get_users(asyncpg_pool):
    async def get_users_from_db():
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM users""")

    return get_users_from_db


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                """SELECT * FROM users WHERE id = $1;""", user_id
            )

    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        id: UUID,
        created_at: datetime.datetime,
        login: EmailStr,
        password: str,
        project_id: UUID,
        env: str,
        domain: UserDomain,
        locktime: datetime.datetime | None,
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                id,
                created_at,
                login,
                password,
                project_id,
                env,
                domain,
                locktime,
            )

    return create_user_in_database


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        app.dependency_overrides[get_async_session] = get_test_session
        yield ac
