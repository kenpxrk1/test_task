import datetime
from httpx import AsyncClient
import pytest
from uuid import uuid4
from api.config import settings


@pytest.mark.asyncio
async def test_acquire_lock(ac: AsyncClient, create_user_in_database):
    user_data = {
        "id": uuid4(),
        "created_at": datetime.datetime.now(),
        "login": "petr@gmail.com",
        "password": "123456",
        "project_id": uuid4(),
        "env": settings.ENV_MODE,
        "domain": "canary",
        "locktime": datetime.datetime.now(),
    }
    await create_user_in_database(**user_data)
    resp = await ac.patch(f"/users/release_lock/{user_data['id']}")
    assert resp.status_code == 200
    user_from_resp = resp.json()
    assert user_from_resp["id"] == str(user_data["id"])
    assert user_from_resp["locktime"] == None
