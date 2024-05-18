#!/usr/bin/env python3
"""
Cache class
"""


import redis
import uuid
from functools import wraps


class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Store an instance of the Redis client as a private variable named _redis.
        Flush the instance using flushdb.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    
    def store(self, data: bytes) -> str:
        """
        Store the input data in Redis using a random key (generated with uuid).
        Return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


def call_history(method):
    """
    Decorator to store input and output history in Redis.
    """
    
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_name = method.__qualname__
        input_key = "{}:inputs".format(method_name)
        output_key = "{}:outputs".format(method_name)

        # Append input arguments to Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function
        result = method(self, *args, **kwargs)

        # Store the output in Redis list
        self._redis.rpush(output_key, result)

        return result
    return wrapper

# Apply call_history decorator to Cache.store
Cache.store = call_history(Cache.store)


def replay(method):
    """
    Display the history of calls for a given method.
    """
    method_name = method.__qualname__
    input_key = "{}:inputs".format(method_name)
    output_key = "{}:outputs".format(method_name)

    # Retrieve input and output lists from Redis
    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for inp, outp in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode()}) -> {outp.decode()}")


# Example usage
if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
    print(local_redis.lrange("Cache.store:inputs", 0, -1))
    print(local_redis.lrange("Cache.store:outputs", 0, -1))
