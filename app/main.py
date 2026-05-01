

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import admin, auth, wallet


@asynccontextmanager
async def lifespan(app: FastAPI):
   

    Base.metadata.create_all(bind=engine)
    yield
   


app = FastAPI(
    title="Digital Wallet API",
    description=(
        "A secure REST API for managing digital wallets. "
        "Supports user registration, JWT authentication, deposits, withdrawals, "
        "and peer-to-peer transfers."
    ),
    version="1.0.0",
    lifespan=lifespan,
)



app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(admin.router)



@app.get("/", tags=["Health"], summary="Health check")
def root():

    return {"status": "ok", "message": "Digital Wallet API is running."}