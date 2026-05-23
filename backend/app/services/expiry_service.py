from sqlalchemy import select
from datetime import datetime

from app.models.reservation import Reservation
from app.models.inventory import Inventory
from app.utils.enums import ReservationStatus


async def cleanup_expired_reservations(db):
    query = select(Reservation).where(
        Reservation.status == ReservationStatus.PENDING,
        Reservation.expires_at < datetime.utcnow(),
    )

    result = await db.execute(query)
    expired = result.scalars().all()

    for reservation in expired:
        inventory_query = select(Inventory).where(
            Inventory.product_id == reservation.product_id,
            Inventory.warehouse_id == reservation.warehouse_id,
        )

        inventory_result = await db.execute(inventory_query)
        inventory = inventory_result.scalar_one()

        inventory.reserved_stock -= reservation.quantity

        reservation.status = ReservationStatus.RELEASED

    await db.commit()