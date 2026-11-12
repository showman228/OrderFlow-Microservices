import pytest


@pytest.mark.asyncio
async def test_get_product_by_id(client, seeded_products) -> None:
    product = seeded_products[0]

    response = await client.get(f"/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["name"] == product.name


@pytest.mark.asyncio
async def test_get_product_by_name(client, seeded_products) -> None:
    product = seeded_products[1]

    response = await client.get(f"/products/names/{product.name}")

    assert response.status_code == 200
    assert response.json()["id"] == product.id
