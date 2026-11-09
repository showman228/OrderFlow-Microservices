import pytest


@pytest.mark.asyncio
async def test_create_category(client) -> None:
    response = await client.post(
        "/categories/create",
        json={
            "name": "Электроника",
            "slug": "electronic",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Электроника"


@pytest.mark.asyncio
async def test_read_category(client) -> None:
    await client.post(
        "/categories/create",
        json={
            "name": "полотенце",
            "slug": "polotenche",
        },
    )

    response = await client.get(
        "/categories/1",
    )

    assert response.status_code == 200
    assert response.json()["name"] == "полотенце"
    assert response.json()["slug"] == "polotenche"