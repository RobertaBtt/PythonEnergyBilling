"""All times are UTC.
We’re only dealing with £ denominated billing.
You only need to handle electricity and gas billing.
Energy is consumed linearly.
The billing date is the last day of the month.
Readings are always taken at midnight.
There is only one meter reading per billing period.
The JSON file structure will remain the same in any follow on exercise."""

"""To get an overview on how Bulb compute the energy Bill, 
I did a fast research on help pages in the Bulb website
From here:
https://help.bulb.co.uk/hc/en-us/articles/115003193451-When-should-I-submit-a-meter-reading-

Ideally the customer should  submit meter readings every month.
That's why it must be avoided to compute for example
energy bills of more than 30 days. 

We'll ask you to send your reading during the 3 days before your payment date. 
This helps make sure your statement is based on up-to-date usage data. 
So if your payment date is on the 5th of the month, 
you should send your reading on the 2nd, 3rd or 4th. 
Otherwise, we'll have to estimate some of your usage """

"""So, if the meter readings is not present, Bulb estimate it, 
based on the previous meter readings

That's why it is needed an algorithm that is capable to estimate the kwh
progression, based on the previous data available.

From here:
https://help.bulb.co.uk/hc/en-us/articles/360017679811-How-do-estimated-meter-readings-work-


All estimated meter readings, no matter what supplier you’re with, 
are based on the historical energy usage of your property. 
The more meter readings received from that property, 
the more accurate those estimated readings are likely to be.

- When we’ll use estimates

To use your meter readings to calculate your statement, 
we need them within the three days before your payment date. 
If you submit them at another time, we’ll need to estimate the 
remaining days of that payment month. 
And if you don’t submit them at all, 
we’ll estimate your usage for the entire month.

If you do submit your meter readings outside of this 
three-day window, or not at all, your statement will 
show this month’s payment is based on an estimated reading.

-------------
That's why in this test is not only required to do date_end - date_begin meter readings, 
but to compute whenever the exact month is not available.
"""

from typing import Dict, List
from load_date_utils import *
from tariff import BULB_TARIFF

def kwh_between(reading_begin: Dict, reading_end: Dict):
    return reading_end["cumulative"] - reading_begin["cumulative"]


def avg_kwh_day(reading_begin: Dict, reading_end: Dict):
    kwh = kwh_between(reading_begin, reading_end)
    days = days_between(to_date(reading_begin["readingDate"]), to_date(reading_end["readingDate"]))
    return kwh // days


"""Giving a list of meter readings, this function retrieves the dates that are useful for the calculation.
    Since 'Energy is consumed linearly' the program does not need to sort the list. 
"""

def get_meterings_bill_date(meterings: List, bill_date: datetime) -> List:
    month_before_bill = minus_one_month(bill_date)
    for index, data in enumerate(meterings):
        date_meter = to_date(data["readingDate"])
        if date_meter.year == month_before_bill.year and date_meter.month == month_before_bill.month:
            # If we are not in the last index of the list:
            if index < (len(meterings) - 1):
                # list slicing + 1 element
                return meterings[index:(index + 2)]
            else:
                return meterings[index]

"""Providing the gap that remains to reach the end of the month,
this function computes:
 - the estimation to cover the end of the month
 - the estimation to cover the begin of the period.
 
In this lastcase the function is more accurate, because I don't want to 
estimate a meter reading, for the begin period, that is less than the last available meter reading
that is at the end of the period.
So I use the function "range", that is perfect for this usecase.
"""
def kwh_between_estimated(reading_begin:Dict, reading_end:Dict, gap_begin, gap_end):
    reading_end_kwh = reading_end["cumulative"]
    reading_begin_kwh = reading_begin["cumulative"]

    average_kwh_day = avg_kwh_day(reading_begin, reading_end)

    # gap_begin are the days that remains to reach the end of first month
    # gap_end are the days that remains to reach the end of the second month

    if gap_end > 0:
        reading_end_kwh += (gap_end * average_kwh_day)
    if gap_begin > 0:
        reading_begin_kwh = range(reading_begin["cumulative"], reading_end["cumulative"],average_kwh_day )[gap_begin]
    return reading_end_kwh - reading_begin_kwh


def get_kwh_days(energy_meterings: List, bill_date: datetime) ->(float, int):

    #meterings is a subset of the whole data set
    meterings = get_meterings_bill_date(energy_meterings, bill_date)
    kwh = 0.
    days = 0
    if meterings is not None:
        month_before_bill = minus_one_month(bill_date)

        gap_begin = days_to_last_day(to_date(meterings[0]["readingDate"]))
        gap_end = days_to_last_day(to_date(meterings[1]["readingDate"]))

        # If there's no need to estimate, because there are no gaps,
        # then the computation is simple meter_reading_end - meter_reading_begin
        if gap_begin == 0 and gap_end == 0:
            kwh = kwh_between(meterings[0], meterings[1])
        else:
            # Else this function helps on retrieving the estimated
            # progression of the kwh
            kwh = kwh_between_estimated(meterings[0], meterings[1],gap_begin, gap_end)

        days = days_between(month_before_bill, bill_date)
    else:
        print("Meter readings not found for the bill_date provided")

    return kwh,days

#The moltiplication is separated. Because the algorithm can change
# Separate the things that vary from what stay the same
# is one of the Clean Code principles.
def get_amount(kwh:int, days:int)->(float, int):

    fixed_amount = (BULB_TARIFF["electricity"]["standing_charge"]/100.0) * days
    total_unit_rate = (BULB_TARIFF["electricity"]["unit_rate"]/100.0) * kwh
    amount = round(fixed_amount + total_unit_rate, 2)
    return amount
