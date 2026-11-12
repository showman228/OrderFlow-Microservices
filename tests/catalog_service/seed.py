from sqlalchemy.ext.asyncio import AsyncSession

from catalog_service.app.models import Category, Product

SEED_CATEGORY_NAME = "машина"
SEED_CATEGORY_SLUG = "cars"


async def seed_category(db: AsyncSession) -> Category:

    category = Category(name=SEED_CATEGORY_NAME, slug=SEED_CATEGORY_SLUG)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def seed_products(db: AsyncSession, count: int = 3) -> list[Product]:

    category = await seed_category(db)

    products = [
        Product(
            name=f"Product-{i + 1}",
            description=f"Description-{i + 1}",
            price=1000 + i + 1,
            category_id=category.id,
        )
        for i in range(count)
    ]
    db.add_all(products)
    await db.commit()

    for product in products:
        await db.refresh(product)

    return products
