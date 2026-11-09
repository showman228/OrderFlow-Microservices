import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from catalog_service.app.models.category import Category
from catalog_service.app.models.product import Product


async def seed_products(db: AsyncSession, count: int = 3) -> list[Product]:
    category = Category(name="машина", slug="cars")
    db.add(category)
    await db.flush()  # получить category.id без commit (id — автоинкремент)

    products = []
    for i in range(count):
        products.append(
            Product(
                name=f"Product-{i + 1}",
                description=f"Description {i + 1}",
                price=1000 + i + 1,
                category_id=category.id,
            )
        )

    db.add_all(products)
    await db.commit()

    for product in products:
        await db.refresh(product)

    return products


@pytest_asyncio.fixture
async def seeded_products(db_session) -> list[Product]:
    return await seed_products(db_session, count=3)


@pytest.mark.asyncio
async def test_get_product_by_id(client, seeded_products) -> None:
    product = seeded_products[0]

    response = await client.get(f"/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["id"] == product.id


@pytest.mark.asyncio
async def test_get_product_by_name(client, seeded_products) -> None:
    product = seeded_products[1]

    response = await client.get(f"/products/names/{product.name}")

    assert response.status_code == 200
    assert response.json()["name"] == product.name
