from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient, get_users):
    response = await ac.post(
        "/users",
        json={
            "login": "user@example.com",
            "password": "string",
            "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "domain": "canary",
        },
    )
    users = await get_users()
    assert len(users) == 1
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_email_duplicate_error(ac: AsyncClient, get_users):
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
    response = await ac.post("/users", json=user_data)
    users = await get_users()
    assert len(users) == 2
    assert response.status_code == 201
    response = await ac.post("/users", json=user_same_data)
    users = await get_users()
    assert len(users) == 2
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_users(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
