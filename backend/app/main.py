from fastapi import FastAPI

from app.api.products import router as product_router
from app.api.warehouses import router as warehouse_router
from app.api.reservations import router as reservation_router

from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base

from app.models import product
from app.models import inventory
from app.models import reservation
from app.models import warehouse


app = FastAPI(title="Allo Reservation System")


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created")


app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(reservation_router)


@app.get("/")
async def root():
    return {"message": "Allo Backend Running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)