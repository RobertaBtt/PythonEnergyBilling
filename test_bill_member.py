import datetime
import unittest

from bill_member import calculate_bill


class TestBillMember(unittest.TestCase):
    def setUp(self) -> None:
        self.member_id = "member-123"
        self.account_id = "ALL"
        self.bill_date = "2017-08-31"

    def test_calculate_bill_for_august(self):
        amount, kwh = calculate_bill(self.member_id, self.account_id,self.bill_date)
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
