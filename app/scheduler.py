from datetime import datetime, timezone


def to_naive_utc(dt: datetime) -> datetime:
    """Convert a timezone-aware datetime to naive UTC."""
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def has_conflict(new_start: datetime, new_end: datetime, existing_bookings: list):
    new_start = to_naive_utc(new_start)
    new_end = to_naive_utc(new_end)
    for booking in existing_bookings:
        existing_start = to_naive_utc(booking.start_time)
        existing_end = to_naive_utc(booking.end_time)

        # Check for overlap
        if (new_start < existing_end) and (new_end > existing_start):
            return True
    return False
