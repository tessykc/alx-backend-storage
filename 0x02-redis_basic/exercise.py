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


def count_calls(method):
    """
    Decorator to count method calls using Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_name = method.__qualname__
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)
    return wrapper

# Apply count_calls decorator to Cache.store
Cache.store = count_calls(Cache.store)


# Example usage
if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
    print(local_redis.get("Cache.store"))  # Check method call count
