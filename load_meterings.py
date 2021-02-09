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


def deserialize_one(meterings:List, account_id:str, service_type: str):
    if meterings is not None and isinstance(meterings, List):
        for metering in meterings:
            if account_id in metering:
                try:
                    meterings_for_account = get(metering, "JSON", account_id)
                    for meterings in meterings_for_account:
                        meter_reading_list = get(meterings, "JSON", service_type)
                    return meter_reading_list

                except Exception as ex:
                    raise ex
            else:
                print("Account",account_id,"not found")
                raise KeyError

def get(readings, format, key):
    deserializer = DESERIALIZERS[format]
    return deserializer(readings, key)
