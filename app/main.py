from fastapi import FastAPI
from app.routers import resources, bookings

app = FastAPI()
app.include_router(resources.router)
app.include_router(bookings.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
