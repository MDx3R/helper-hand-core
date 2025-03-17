from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

def get_current_time() -> datetime:
    return datetime.now(ZoneInfo("Europe/Moscow"))

def is_current_time_valid_for_reply(date: date) -> bool:
    return date-timedelta(hours=2) > get_current_time()