from fastapi import FastAPI
from app.routers import resources, bookings, auth
from app.database import Base, engine
from contextlib import asynccontextmanager


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
