DESERIALIZERS = dict()


def register(func):
    """Register a function that can deserialize different formats"""
    DESERIALIZERS[func.__name__] = func
    return func

