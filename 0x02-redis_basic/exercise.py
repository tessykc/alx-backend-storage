#!/usr/bin/env python3
"""
Cache class
"""


import uuid
import redis
from typing import Callable, Optional
from functools import wraps


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
    self._call_counts = {}  # Dictionary to store method call counts

  
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
    
    
    @count_calls
    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[bytes | str | int | float]:
    """
    Retrieves data from Redis for the provided key and converts it using the optional callable.

    Args:
        key (str): The key to retrieve data for.
        fn (Callable, optional): A function to convert the retrieved data (default: None).

    Returns:
        Optional[bytes | str | int | float]: The retrieved data, converted using the function if provided,
                                            or None if the key doesn't exist.
    """

    data = self._redis.get(key)
    if data is None:
      return None

    # Convert data if a conversion function is provided
    if fn:
      return fn(data)

    # Handle basic data types returned by Redis (bytes, int)
    try:
      # Try converting to integer first
      return int(data)
    except ValueError:
      pass

    # If conversion fails, return bytes as default
    return data


  def get_str(self, key: str) -> Optional[str]:
    """
    Retrieves data from Redis for the provided key and converts it to a string using UTF-8 decoding.

    Args:
        key (str): The key to retrieve data for.

    Returns:
        Optional[str]: The retrieved data as a string, or None if the key doesn't exist.
    """

    return self.get(key, lambda d: d.decode("utf-8"))


  def get_int(self, key: str) -> Optional[int]:
    """
    Retrieves data from Redis for the provided key and converts it to an integer.

    Args:
        key (str): The key to retrieve data for.

    Returns:
        Optional[int]: The retrieved data as an integer, or None if the key doesn't exist or conversion fails.
    """

    return self.get(key, int)
    
  
  def _count_call(self, method_name):
    """
    Increments the call count for the specified method.

    Args:
        method_name (str): The qualified name of the method.
    """

    self._call_counts[method_name] = self._call_counts.get(method_name, 0) + 1

  
  def get_call_count(self, method_name):
    """
    Retrieves the call count for the specified method.

    Args:
        method_name (str): The qualified name of the method.

    Returns:
        int: The call count for the method, or 0 if not called.
    """

    return self._call_counts.get(method_name, 0)

  def count_calls(method):
    """
    Decorator to count calls to a method and store the count in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """

  
  @wraps(method)
  def wrapper(self, *args, **kwargs):
    # Get the qualified method name
    method_name = method.__qualname__

    # Increment the call count
    self._count_call(method_name)

    # Call the original method
    result = method(self, *args, **kwargs)

    return result

  return wrapper


if __name__ == "__main__":
  cache = Cache()

  TEST_CASES = {
      b"foo": None,
      123: int,
      "bar": lambda d: d.decode("utf-8")
  }

  for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
