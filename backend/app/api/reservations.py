from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.database import get_db
from app.schemas.reservation import ReservationCreate
from app.models.reservation import Reservation
from app.models.inventory import Inventory
from app.services.reservation_service import create_reservation
from app.services.expiry_service import cleanup_expired_reservations
from app.utils.enums import ReservationStatus

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])


@router.post("")
async def reserve_stock(
    payload: ReservationCreate,
    db: AsyncSession = Depends(get_db),
):
    await cleanup_expired_reservations(db)

    reservation = await create_reservation(db, payload)

    return reservation


@router.post("/{reservation_id}/confirm")
async def confirm_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(Reservation).where(Reservation.id == reservation_id)

    result = await db.execute(query)
    reservation = result.scalar_one_or_none()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Reservation expired")

    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(status_code=400, detail="Invalid reservation")

    inventory_query = select(Inventory).where(
        Inventory.product_id == reservation.product_id,
        Inventory.warehouse_id == reservation.warehouse_id,
    )

    inventory_result = await db.execute(inventory_query)
    inventory = inventory_result.scalar_one()

    inventory.total_stock -= reservation.quantity
    inventory.reserved_stock -= reservation.quantity

    reservation.status = ReservationStatus.CONFIRMED

    await db.commit()

    return {"message": "Reservation confirmed"}
