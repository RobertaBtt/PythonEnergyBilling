import unittest

from account import Account
from load_readings import get_readings

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account()
        self.readings = get_readings()
        self.account.readings = self.readings

    def testInstance(self):
        assert self.account is not None
        assert self.account.readings is not None
        assert len(self.account.readings) !=0