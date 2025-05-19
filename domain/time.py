from datetime import date, datetime, timezone, time

TIMEZONE = timezone.utc


def get_current_time() -> datetime:
    return datetime.now(TIMEZONE)


def combine_time(date: date, tm: time) -> datetime:
    return datetime.combine(date, tm, tzinfo=TIMEZONE)
