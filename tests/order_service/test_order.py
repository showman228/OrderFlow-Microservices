import pytest


@pytest.mark.asyncio
async def test_get_all_orders(client, seeded_orders) -> None:
    response = await client.get("/orders/")

    assert response.status_code == 200
    assert len(response.json()) == len(seeded_orders)


@pytest.mark.asyncio
async def test_get_order_by_id(client, seeded_orders) -> None:
    order = seeded_orders[0]

    response = await client.get(f"/orders/{order.id}")

    assert response.status_code == 200
    assert response.json()["id"] == order.id


@pytest.mark.asyncio
async def test_get_orders_by_user_id(client, seeded_orders) -> None:
    order = seeded_orders[0]

    response = await client.get(f"/orders/users/{order.user_id}")

    assert response.status_code == 200
    assert len(response.json()) == 1
