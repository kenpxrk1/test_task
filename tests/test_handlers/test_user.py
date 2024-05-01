import json
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient, get_user_from_database, get_users):
    user_data = {
        "login": "user@example.com",
        "password": "string",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "domain": "canary",
    }
    response = await ac.post("/users", data=json.dumps(user_data))
    user_from_resp = response.json()
    assert response.status_code == 201
    user_from_db = await get_user_from_database(user_from_resp["id"])
    assert len(user_from_db) == 1


@pytest.mark.asyncio
async def test_create_user_email_duplicate_error(
    ac: AsyncClient, get_user_from_database
):
    user_data = {
        "login": "user2@example.com",
        "password": "string",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "domain": "canary",
    }
    user_same_data = {
        "login": "user2@example.com",
        "password": "123456",
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "domain": "regular",
    }
    response = await ac.post("/users", data=json.dumps(user_data))
    user_from_resp = response.json()
    assert response.status_code == 201
    user_from_db = await get_user_from_database(user_from_resp["id"])
    assert len(user_from_db) == 1
    response = await ac.post("/users", data=json.dumps(user_same_data))
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_users(ac: AsyncClient, get_users):
    response = await ac.get("/users")
    assert response.status_code == 200
    users = await get_users()
    assert len(users) != None
