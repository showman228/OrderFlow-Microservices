import pytest

from user_service.app.core.security import verify_password


@pytest.mark.asyncio
async def test_register_user(client) -> None:
    response = await client.post(
        "/users/register",
        json={
            "email": "test@mail.com",
            "username": "bob",
            "firstname": "alex",
            "password": "1234",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["email"] == "test@mail.com"
    assert body["username"] == "bob"
    assert verify_password("1234", body["password_hash"])


@pytest.mark.asyncio
async def test_get_current_user(client, seeded_users) -> None:
    user = seeded_users[1]

    response = await client.get("/users/me", auth=(user.username, "1232"))

    assert response.status_code == 200
    assert response.json()["id"] == user.id
    assert response.json()["email"] == user.email


@pytest.mark.asyncio
async def test_get_all_users(client, seeded_users) -> None:
    response = await client.get("/users/all")

    assert response.status_code == 200
    assert len(response.json()) == len(seeded_users)
