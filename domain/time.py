from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_time() -> datetime:
    return datetime.now(ZoneInfo("Europe/Moscow"))
