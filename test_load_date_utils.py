import unittest
from load_readings import get_readings

from load_dateutils import to_date

class TestLoadMeterings(unittest.TestCase):

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