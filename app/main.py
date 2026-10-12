from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, bookings, resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(resources.router)
app.include_router(bookings.router)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
