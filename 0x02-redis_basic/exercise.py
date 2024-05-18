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


def replay(cache: redis.Redis, function_name: str) -> None:
  """
  Displays the call history for a function using Redis.

  Args:
      cache (redis.Redis): The Redis client connection.
      function_name (str): The qualified name of the function.
  """

  # Construct the input and output key patterns
  input_key_pattern = f"{function_name}:inputs:*"
  output_key_pattern = f"{function_name}:outputs:*"

  # Retrieve input and output lists using scan
  input_keys, cursor = cache.scan(match=input_key_pattern, cursor=0, count=10)
  output_keys, _ = cache.scan(match=output_key_pattern, cursor=cursor, count=10)

  # Combine input and output keys while maintaining order
  call_keys = sorted(zip(input_keys, output_keys))

  # Print the call history
  print(f"{function_name} was called {len(call_keys)} times:")
  for i, (input_key, output_key) in enumerate(call_keys):
    inputs = cache.lrange(input_key, 0, -1)
    output = cache.get(output_key)
    print(f"  Call {i+1}:")
    print(f"    Inputs: {inputs}")
    print(f"    Output: {output.decode('utf-8') if output else None}")


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
