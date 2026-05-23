from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.models.inventory import Inventory
from app.models.reservation import Reservation
from app.utils.enums import ReservationStatus


async def create_reservation(db, payload):
    try:
        query = (
            select(Inventory)
            .where(
                Inventory.product_id == payload.product_id,
                Inventory.warehouse_id == payload.warehouse_id,
            )
            .with_for_update()
        )

        result = await db.execute(query)
        inventory = result.scalar_one_or_none()

        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")

        available_stock = inventory.total_stock - inventory.reserved_stock

        if available_stock < payload.quantity:
            raise HTTPException(status_code=409, detail="Not enough stock")

        inventory.reserved_stock += payload.quantity

        reservation = Reservation(
            product_id=payload.product_id,
            warehouse_id=payload.warehouse_id,
            quantity=payload.quantity,
            status=ReservationStatus.PENDING,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
        )

        db.add(reservation)

        await db.commit()
        await db.refresh(reservation)

        return reservation

    except SQLAlchemyError:
        await db.rollback()
        raise