import datetime
from dateutil.parser import parse


def to_date(string_date: str) -> datetime:
    try:
        return parse(string_date).date()
    except Exception as ex:
        raise ex