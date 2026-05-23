from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db
from app.models.warehouse import Warehouse

router = APIRouter(prefix="/api/warehouses", tags=["Warehouses"])


@router.get("")
async def get_warehouses(db: AsyncSession = Depends(get_db)):
    query = select(Warehouse)

    result = await db.execute(query)

    return result.scalars().all()