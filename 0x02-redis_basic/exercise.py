#!/usr/bin/env python3
"""
Cache class
"""


import uuid
import redis

class Cache:
  """
  A simple cache class that utilizes Redis for storage.
  """

  def __init__(self):
    """
    Initializes the cache with a Redis client and flushes the existing database.
    """
    self._redis = redis.Redis()  # Private attribute for Redis client
    self._redis.flushdb()  # Flush the Redis database

  def store(self, data: bytes | str | int | float) -> str:
    """
    Stores the provided data in Redis and returns the generated key.

    Args:
        data (bytes | str | int | float): The data to be stored in Redis.

    Returns:
        str: The generated random key used to store the data.
    """

    key = str(uuid.uuid4())  # Generate a random key using UUID
    self._redis.set(key, data)  # Store the data with the generated key
    return key

if __name__ == "__main__":
  cache = Cache()

  data = b"hello"
  key = cache.store(data)
  print(key)

  local_redis = redis.Redis()
  print(local_redis.get(key))
