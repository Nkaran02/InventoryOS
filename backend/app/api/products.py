from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("")
async def get_products(db: AsyncSession = Depends(get_db)):
    query = select(Product).options(selectinload(Product.inventories))

    result = await db.execute(query)
    products = result.scalars().all()

    response = []

    for product in products:
        warehouses = []

        for inventory in product.inventories:
            warehouses.append(
                {
                    "warehouse_id": inventory.warehouse_id,
                    "available_stock": inventory.total_stock
                    - inventory.reserved_stock,
                }
            )

        response.append(
            {
                "id": product.id,
                "name": product.name,
                "warehouses": warehouses,
            }
        )

    return response