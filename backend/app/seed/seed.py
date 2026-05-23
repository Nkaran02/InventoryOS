import asyncio

from app.core.database import engine
from app.core.database import Base
from app.core.database import AsyncSessionLocal

from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        warehouse1 = Warehouse(name="Bangalore Warehouse")
        warehouse2 = Warehouse(name="Mumbai Warehouse")

        session.add_all([warehouse1, warehouse2])

        await session.flush()

        product1 = Product(name="iPhone 15")
        product2 = Product(name="MacBook Air")

        session.add_all([product1, product2])

        await session.flush()

        inventory1 = Inventory(
            product_id=product1.id,
            warehouse_id=warehouse1.id,
            total_stock=10,
            reserved_stock=0,
        )

        inventory2 = Inventory(
            product_id=product2.id,
            warehouse_id=warehouse2.id,
            total_stock=5,
            reserved_stock=0,
        )

        session.add_all([inventory1, inventory2])

        await session.commit()


asyncio.run(seed())