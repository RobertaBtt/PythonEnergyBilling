import unittest
from load_readings import get_readings
from load_meterings import deserialize_one

class TestLoadMeterings(unittest.TestCase):

    def setUp(self) -> None:
        self.readings = get_readings()
        self.account_id="account-abc"
        self.service_type="electricity"

    def testDeserializeOne(self):
        content = self.readings["member-123"]
        result = deserialize_one(content, self.account_id, self.service_type)
        assert result is not None
        assert len(result) == 14

    def testDeserializeOneAccountUnavailable(self):
        content = self.readings["member-123"]
        with self.assertRaises(KeyError):
            deserialize_one(content, "account_fake", self.service_type)

    def testDeserializeOneServiceTypeNotValid(self):
        content = self.readings["member-123"]
        with self.assertRaises(KeyError):
            deserialize_one(content, "account-abc", "smarthome")

    def testDeserializeOneEmpty(self):
        assert deserialize_one(None, "account-abc", "smarthome") == None

    def testDeserializeOneNotAList(self):
        assert deserialize_one(1, "account-abc", "smarthome") == None

