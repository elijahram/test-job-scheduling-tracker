from app.models import Booking, Resource
from app.schemas import BookingCreate, BookingOut
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.scheduling import has_conflict

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=list[BookingOut])
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings


@router.post("/", response_model=BookingOut)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    if booking.end_time <= booking.start_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time.",
        )
    if not db.query(Resource).filter(Resource.id == booking.resource_id).first():
        raise HTTPException(
            status_code=404,
            detail=f"Resource with id '{booking.resource_id}' not found.",
        )
    existing_bookings = (
        db.query(Booking).filter(Booking.resource_id == booking.resource_id).all()
    )
    if has_conflict(booking.start_time, booking.end_time, existing_bookings):
        raise HTTPException(
            status_code=409,
            detail="Booking conflicts with an existing booking.",
        )
    db_booking = Booking(**booking.model_dump())
    try:
        db.add(db_booking)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Booking could not be created due to a database error.",
        )
    db.refresh(db_booking)
    return db_booking
