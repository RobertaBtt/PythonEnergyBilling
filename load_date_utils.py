import datetime
from dateutil.parser import parse
import dateutil.relativedelta
import calendar


def to_date(string_date: str) -> datetime:
    try:
        return parse(string_date).date()
    except Exception as ex:
        raise ex


def is_last_day(date_: datetime) -> bool:
    if calendar.monthrange(date_.year, date_.month)[1] == date_.day:
        return True
    return False


def days_to_last_day(date_: datetime) -> int:
    if is_last_day(date_):
        return 0
    else:
        return calendar.monthrange(date_.year, date_.month)[1] - date_.day


def days_between(date_before:datetime, date_after:datetime) -> int:
    try:
        delta_days = (date_after - date_before).days
    except ValueError as ex:
        raise ex
    return delta_days


def minus_one_month(date_: datetime) -> datetime:
    try:
        new_date = date_ + dateutil.relativedelta.relativedelta(months=-1)
        #Ensure we go to the last day of the previous month.
        new_date = new_date + dateutil.relativedelta.relativedelta(days=days_to_last_day(new_date))
    except ValueError as ex:
        raise ex
    return new_date

