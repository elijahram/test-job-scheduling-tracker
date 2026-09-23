from datetime import datetime


def has_conflict(new_start: datetime, new_end: datetime, existing_bookings: list):

    for booking in existing_bookings:
        existing_start = booking.start_time
        existing_end = booking.end_time

        # Check for overlap
        if (new_start < existing_end) and (new_end > existing_start):
            return True
    return False
