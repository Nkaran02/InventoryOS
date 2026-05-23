from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.utils.enums import ReservationStatus


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    quantity = Column(Integer, nullable=False)

    status = Column(
        Enum(ReservationStatus),
        default=ReservationStatus.PENDING,
    )

    expires_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
    warehouse = relationship("Warehouse")