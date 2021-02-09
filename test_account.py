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
        assert len(self.account.readings) != 0

    def testInstanceSetMember(self):
        self.account.member = "member_id"
        assert self.account.member == "member_id"

    def testInstanceSetAccountId(self):
        self.account.account_id = "account-abc"
        assert self.account.account_id == "account-abc"

    def testInstanceSetServiceType(self):
        self.account.service_type = "electricity"
        assert self.account.service_type == "electricity"