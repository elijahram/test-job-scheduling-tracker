from datetime import datetime, timezone
from types import SimpleNamespace
from app.scheduling import has_conflict


def test_conflict_when_windows_overlap():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 9, 30)
    new_end = datetime(2026, 9, 24, 10, 30)
    assert has_conflict(new_start, new_end, existing_bookings) is True


def test_no_conflict_when_no_existing_bookings():
    existing_bookings = []
    new_start = datetime(2026, 9, 24, 9, 0)
    new_end = datetime(2026, 9, 24, 10, 0)
    assert has_conflict(new_start, new_end, existing_bookings) is False


def test_no_conflict_when_back_to_back():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 10, 0)
    new_end = datetime(2026, 9, 24, 11, 0)
    assert has_conflict(new_start, new_end, existing_bookings) is False


def test_no_conflict_when_new_booking_ends_at_existing_start():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 8, 0)
    new_end = datetime(2026, 9, 24, 9, 0)
    assert has_conflict(new_start, new_end, existing_bookings) is False


def test_conflict_when_new_window_fully_contains_existing():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 8, 55)
    new_end = datetime(2026, 9, 24, 10, 5)
    assert has_conflict(new_start, new_end, existing_bookings) is True


def test_conflict_when_existing_fully_contains_new():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 9, 15)
    new_end = datetime(2026, 9, 24, 9, 45)
    assert has_conflict(new_start, new_end, existing_bookings) is True


def test_conflict_detected_when_not_first_booking_in_list():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 8, 0),
            end_time=datetime(2026, 9, 24, 9, 0),
        ),
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 30),
            end_time=datetime(2026, 9, 24, 10, 30),
        ),
    ]
    new_start = datetime(2026, 9, 24, 9, 45)
    new_end = datetime(2026, 9, 24, 10, 15)
    assert has_conflict(new_start, new_end, existing_bookings) is True


def test_no_conflict_detected_when_not_first_booking_in_list():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 8, 0),
            end_time=datetime(2026, 9, 24, 9, 0),
        ),
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 10, 0),
            end_time=datetime(2026, 9, 24, 11, 0),
        ),
    ]
    new_start = datetime(2026, 9, 24, 9, 15)
    new_end = datetime(2026, 9, 24, 9, 45)
    assert has_conflict(new_start, new_end, existing_bookings) is False


def test_conflict_with_same_start_and_end_times():
    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),
            end_time=datetime(2026, 9, 24, 10, 0),
        )
    ]
    new_start = datetime(2026, 9, 24, 9, 0)
    new_end = datetime(2026, 9, 24, 10, 0)
    assert has_conflict(new_start, new_end, existing_bookings) is True


def test_conflict_with_naive_and_aware_datetimes():
    from datetime import timezone

    existing_bookings = [
        SimpleNamespace(
            start_time=datetime(2026, 9, 24, 9, 0),  # naive datetime
            end_time=datetime(2026, 9, 24, 10, 0),  # naive datetime
        )
    ]
    new_start = datetime(2026, 9, 24, 9, 30, tzinfo=timezone.utc)
    new_end = datetime(2026, 9, 24, 10, 30, tzinfo=timezone.utc)
    assert has_conflict(new_start, new_end, existing_bookings) is True
