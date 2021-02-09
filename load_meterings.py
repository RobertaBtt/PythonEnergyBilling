DESERIALIZERS = dict()

from typing import List

def register(func):
    """Register a function that can deserialize different formats"""
    DESERIALIZERS[func.__name__] = func
    return func

@register
def JSON(readings, key):
    if key in readings:
        return readings[key]
    else:
        print(key, " not found")
        raise KeyError

@register
def YAML(readings, key):
    raise NotImplementedError


def deserialize_list(readings:List, member_id:str, account_id:str, service_type):
    account_list = []
    try:
        member_id = get(readings, "JSON", member_id)
        if account_id == "ALL":
            # This is a list of dictionaries with key <<account_id>>
            for accounts in member_id:
                #A member can have more than one account
                for account_id, values in accounts.items():
                    account_list.append(deserialize_one(member_id, account_id, service_type))
        else:
            return deserialize_one(member_id, account_id, service_type)
        return account_list

    except Exception as ex:
        raise ex

def deserialize_one(readings:List, account_id:str, service_type: str):
    if readings is not None and isinstance(readings, List):
        for metering in readings:
            if account_id in metering:
                try:
                    meterings_for_account = get(metering, "JSON", account_id)
                    for readings in meterings_for_account:
                        meter_reading_list = get(readings, "JSON", service_type)
                    return meter_reading_list

                except Exception as ex:
                    raise ex
            else:
                print("Account",account_id,"not found")
                raise KeyError

def get(readings, format, key):
    deserializer = DESERIALIZERS[format]
    return deserializer(readings, key)
