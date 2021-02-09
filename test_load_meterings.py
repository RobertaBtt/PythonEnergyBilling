import unittest
from load_readings import get_readings
from load_meterings import deserialize_one
from load_meterings import deserialize_list

class TestLoadMeterings(unittest.TestCase):

    def setUp(self) -> None:
        self.readings = get_readings()
        self.account_id = "account-abc"
        self.service_type = "electricity"
        self.account_fake = "account_fake"
        self.member_id = "member-123"
        self.service_fake = "smarthome"
        self.all_accounts = "ALL"

    def testDeserializeOne(self):
        content = self.readings[self.member_id]
        result = deserialize_one(content, self.account_id, self.service_type)
        assert result is not None
        assert len(result) == 14

    def testDeserializeOneAccountUnavailable(self):
        content = self.readings[self.member_id]
        with self.assertRaises(KeyError):
            deserialize_one(content, self.account_fake, self.service_type)

    def testDeserializeOneServiceTypeNotValid(self):
        content = self.readings[self.member_id]
        with self.assertRaises(KeyError):
            deserialize_one(content, self.account_id, self.service_fake)

    def testDeserializeOneEmpty(self):
        assert deserialize_one(None, self.account_id, self.service_fake) is None

    def testDeserializeOneNotAList(self):
        assert deserialize_one(1, self.account_id, self.service_fake) is None

    def testDeserializeList(self):
        result = deserialize_list(self.readings, self.member_id, self.account_id,  self.service_type)
        assert result is not None
        assert(len(result) == 14)

    def testDeserializeListAllAccounts(self):
        #When accounts are "ALL", the result is a list of the list of the accounts.
        result = deserialize_list(self.readings, self.member_id, self.all_accounts,  self.service_type)
        assert result is not None
        #This is a list of lists
        assert(len(result) == 1)
        assert (len(result[0]) == 14)