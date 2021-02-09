import unittest
from load_readings import get_readings
from load_meterings import deserialize_one
from load_meterings import getAccountMeterReadings
from account import Account

class TestLoadMeterings(unittest.TestCase):

    def setUp(self) -> None:
        self.readings = get_readings()
        self.account = Account()
        self.account.service_type = "electricity"
        self.account.member_id = "member-123"
        self.account.readings = get_readings()
        self.account.account_id = "account-abc"

    def testDeserializeOne(self):
        content = self.readings[self.account.member_id]
        result = deserialize_one(content, self.account.account_id, self.account.service_type)
        assert result is not None
        assert len(result) == 14

    def testDeserializeOneAccountUnavailable(self):
        content = self.readings[self.account.member_id]
        self.account.account_id = "fakeAccount"
        with self.assertRaises(KeyError):
            deserialize_one(content, self.account.account_id, self.account.service_type)

    def testDeserializeOneServiceTypeNotValid(self):
        content = self.readings[self.account.member_id]
        self.account.service_type = "smartHome"
        with self.assertRaises(KeyError):
            deserialize_one(content, self.account.account_id, self.account.service_type)

    def testDeserializeOneEmpty(self):
        self.account.service_type = "smartHome"
        assert deserialize_one(None, self.account.account_id, self.account.service_type) is None

    def testDeserializeOneNotAList(self):
        self.account.service_type = "smartHome"
        assert deserialize_one(1, self.account.account_id, self.account.service_type) is None

    def testDeserializeList(self):
        result = getAccountMeterReadings(self.account)
        assert result is not None
        assert(len(result) == 14)

    def testDeserializeListAllAccounts(self):
        #When accounts are "ALL", the result is a list of the list of the accounts.
        self.account.account_id = "ALL"
        result = getAccountMeterReadings(self.account)
        assert result is not None
        #This is a list of lists
        assert(len(result) == 1)
        assert (len(result[0]) == 14)