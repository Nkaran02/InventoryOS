from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int


class ReservationResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    quantity: int
    status: str
    expires_at: datetime

    class Config:
        from_attributes = True