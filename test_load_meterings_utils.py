import unittest
from load_readings import get_readings
from load_meterings import deserialize_one
from load_meterings import getAccountMeterReadings
from load_meterings_utils import *
from account import Account

class TestLoadMeteringsUtils(unittest.TestCase):

    def setUp(self) -> None:
        #Exact of some meter readings
        self.reading_begin = {"cumulative": 18002, "readingDate": "2017-05-08T00:00:00.000Z", "unit": "kWh"}
        self.reading_end = {"cumulative": 18270, "readingDate": "2017-06-18T00:00:00.000Z", "unit": "kWh"}

        #Whole meter reading list
        self.readings = get_readings()
        self.account = Account()
        self.account.service_type = "electricity"
        self.account.member_id = "member-123"
        self.account.readings = get_readings()
        self.account.account_id = "account-abc"


        self.meter_readings_list = getAccountMeterReadings(self.account)

    def testKwhBetween(self):
        result = kwh_between(self.reading_begin, self.reading_end)
        assert result == 268
    
    def testAvgKwhPerDay(self):
        result = avg_kwh_day(self.reading_begin, self.reading_end)
        days = days_between(to_date(self.reading_begin["readingDate"]), to_date(self.reading_end["readingDate"]))
        kwh = kwh_between(self.reading_begin, self.reading_end)
        assert result == (kwh // days)

    def testMeteringsBillDates(self):
        billing_date = to_date("2017-08-31")
        result = get_meterings_bill_date(self.meter_readings_list, billing_date)
        assert len(result) == 2
        assert result[0] == {'cumulative': 18453, 'readingDate': '2017-07-31T00:00:00.000Z', 'unit': 'kWh'}
        assert result[1] == {'cumulative': 18620, 'readingDate': '2017-08-31T00:00:00.000Z', 'unit': 'kWh'}

    def testMeteringsBillDates(self):
        billing_date = to_date("2017-04-30")
        result = get_meterings_bill_date(self.meter_readings_list, billing_date)
        assert len(result) == 2
        assert result[0] == {'cumulative': 17580, 'readingDate': '2017-03-28T00:00:00.000Z', 'unit': 'kWh'}
        assert result[1] == {'cumulative': 17759, 'readingDate': '2017-04-15T00:00:00.000Z', 'unit': 'kWh'}

    def testMeteringsBillDates2(self):
        billing_date = to_date("2018-01-23")
        result = get_meterings_bill_date(self.meter_readings_list, billing_date)
        assert len(result) == 2
        assert result[0] == {'cumulative': 19517, 'readingDate': '2017-12-31T00:00:00.000Z', 'unit': 'kWh'}
        assert result[1] == {'cumulative': 19757, 'readingDate': '2018-01-23T00:00:00.000Z', 'unit': 'kWh'}

    def testKwhBetweenEstimated(self):
        billing_date = to_date("2018-01-23")
        result = get_meterings_bill_date(self.meter_readings_list, billing_date)
        # gap_begin are the days that remains to reach the end of first month
        gap_begin = days_to_last_day(to_date(result[0]["readingDate"]))
        # gap_end are the days that remains to reach the end of the second month
        gap_end = days_to_last_day(to_date(result[1]["readingDate"]))

        result = kwh_between_estimated(result[0], result[1], gap_begin, gap_end)
        assert result == 320

    def testKwhBetweenEstimatedApril2017(self):
        billing_date = to_date("2017-04-30")
        # 17759 - 17580 = 179
        # between 2017-04-15 and 2017-03-28 there are 18 days
        # the average consumption in this period is: 179 // 18 = 9 kwh per day
        readings_bill_date = get_meterings_bill_date(self.meter_readings_list, billing_date)
        gap_begin = days_to_last_day(to_date(readings_bill_date[0]["readingDate"]))
        gap_end = days_to_last_day(to_date(readings_bill_date[1]["readingDate"]))
        # estimate begin = 17580 + (9 * 3) = 17607
        # estimate_end = 17759 + (9*15) = 17894
        # final result = 17894 -  17607 = 287

        kwh_estimated = kwh_between_estimated(readings_bill_date[0], readings_bill_date[1],gap_begin, gap_end )
        assert kwh_estimated == 287

    def testKwhBetweenEstimatedMay2017(self):
        billing_date = to_date("2017-05-30")
        # 18002 - 17759 = 243
        # 23 days
        # the average consumption in this period is: 179 // 23 = 10 kwh per day
        readings_bill_date = get_meterings_bill_date(self.meter_readings_list, billing_date)
        gap_begin = days_to_last_day(to_date(readings_bill_date[0]["readingDate"]))
        gap_end = days_to_last_day(to_date(readings_bill_date[1]["readingDate"]))
        # estimate begin = 17759 + (10 * 15) = 17909
        # estimate_end = 18002 + (10*23) = 18232
        # final result = 18232 - 17909 = 323

        kwh_estimated = kwh_between_estimated(readings_bill_date[0], readings_bill_date[1], gap_begin,gap_end)
        assert kwh_estimated == 323


    def testKwhBetweenEstimatedJune2017(self):
        billing_date = to_date("2017-06-30")
        # 18270 - 18002 = 268
        #  35 days
        # the average consumption in this period is: 268 // 35 = 6 kwh per day
        readings_bill_date = get_meterings_bill_date(self.meter_readings_list, billing_date)
        gap_begin = days_to_last_day(to_date(readings_bill_date[0]["readingDate"]))
        gap_end = days_to_last_day(to_date(readings_bill_date[1]["readingDate"]))
        # estimate begin = 18002 + (6 * 23) = 18140
        # estimate_end = 18270 + (6*12) = 18342
        # final result = 18342 - 18140 = 202

        kwh_estimated = kwh_between_estimated(readings_bill_date[0], readings_bill_date[1], gap_begin,gap_end)
        assert kwh_estimated == 202


    def testKwhBetweenWholePeriod(self):
        # for the all available readings
        reading_begin = self.meter_readings_list[0]
        reading_end = self.meter_readings_list[-1]
        # 20600 - 17580 = 3020
        kwh_total = kwh_between(reading_begin, reading_end)
        assert kwh_total == 3020

    def testGetKwhDays(self):
        energy_meterings = getAccountMeterReadings(self.account)
        billing_date = to_date("2017-08-31")
        kwh, days = get_kwh_days(energy_meterings, billing_date)
        # kwh are: 18620 - 18453 = 167
        assert (kwh, days) == (167,31)

    def testGetAmount(self):
        energy_meterings = getAccountMeterReadings(self.account)
        billing_date = to_date("2017-08-31")
        kwh, days = get_kwh_days(energy_meterings, billing_date)
        amount = round(((24.56/100.0)*days) + ((11.949/100.0)*kwh), 2)
        assert get_amount(kwh, days) == amount

    def testGetAmount(self):
        energy_meterings = getAccountMeterReadings(self.account)
        billing_date = to_date("2017-09-30")
        kwh, days = get_kwh_days(energy_meterings, billing_date)
        amount = 29.12
        assert get_amount(kwh, days) == amount
