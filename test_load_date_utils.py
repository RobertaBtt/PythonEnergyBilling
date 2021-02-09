import unittest

from load_date_utils import *

class TestLoadDateUtils(unittest.TestCase):

    def testParse(self):
        date_test = "2017-09-08"
        assert to_date(date_test).day == 8
        assert to_date(date_test).month == 9
        assert to_date(date_test).year == 2017

    def testParseWrong(self):
        date_test = "2017-09-90"
        with self.assertRaises(Exception):
            to_date(date_test)

    def testParseEmpty(self):
        date_test = ""
        with self.assertRaises(Exception):
            to_date(date_test)

    def testLastDay(self):
        date_test = "2020-08-31"
        assert is_last_day(to_date(date_test))

    def testNotLastDay(self):
        date_test = "2020-08-15"
        assert not is_last_day(to_date(date_test))

    def testDaysToLastDay(self):
        date_test = to_date("2017-03-28")
        assert days_to_last_day(date_test) == 3

    def testPreviousMonthLastDay(self):
        date_test = "2017-09-09"
        result = minus_one_month(to_date(date_test))
        assert result.year == 2017
        assert result.month == 8
        assert result.day == 31

    def testDaysBetween(self):
        date_test_begin = to_date("2017-04-15")
        date_test_end = to_date("2017-05-08")
        assert days_between(date_test_begin, date_test_end) == 23