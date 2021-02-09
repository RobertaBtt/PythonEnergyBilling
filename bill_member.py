from load_meterings_utils import *
from load_meterings import *
from load_readings import get_readings
from account import Account

def _prepare_account_instance(member_id:str, account_id: str) -> Account:
    account = Account()
    account.service_type = "electricity"
    account.member_id = member_id
    account.readings = get_readings()
    account.account_id = account_id
    return account

def calculate_bill(member_id=None, account_id=None, bill_date=None):
    amount = 0.
    kwh = 0
    days = 0
    if member_id is not None and bill_date is not None:
        try:
            billing_date = to_date(bill_date)

            energy_meterings = getAccountMeterReadings(_prepare_account_instance(member_id, account_id))
            #ALL accounts
            if isinstance(energy_meterings[0], list):
                for energy in energy_meterings:
                    result = get_kwh_days(energy, billing_date)
                    kwh += result[0]
                    days += result[1]

            else:
                (kwh, days) = get_kwh_days(energy_meterings, billing_date)

        except Exception as ex:
            print(ex, "\n(kwh= 0 and amount=0 will be returned)")

    amount = get_amount(kwh, days)

    return amount, kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function."""
    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
