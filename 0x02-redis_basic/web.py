#!/usr/bin/env python3
""" 
web
"""

import requests
import redis
from functools import wraps
from typing import Optional

# Redis connection details (replace with your own)
REDIS_HOST = "localhost"
REDIS_PORT = 6379

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def count_and_cache(cache_expire_seconds: int = 10):
  """
  Decorator to count URL access and cache the result using Redis.

  Args:
      cache_expire_seconds (int, optional): The expiration time for the cached response in seconds (default: 10).

  Returns:
      Callable: The decorated function.
  """

  
  def decorator(func):
    @wraps(func)
    def wrapper(url: str) -> Optional[str]:
      # Construct the cache key
      cache_key = f"count:{url}"

      # Check if the response is cached
      cached_response = cache.get(cache_key)
      if cached_response:
        return cached_response.decode("utf-8")

      # Fetch the response if not cached
      response = func(url)
      if response is not None:
        # Increment access count for the URL
        cache.incr(cache_key)
        # Set the cache expiration time
        cache.expire(cache_key, cache_expire_seconds)
        return response.text

      return None

    return wrapper

  return decorator


@count_and_cache()
def get_page(url: str) -> Optional[str]:
  """
  Fetches the HTML content of a URL using requests and returns it.

  Args:
      url (str): The URL to fetch.

  Returns:
      Optional[str]: The HTML content of the URL, or None if the request fails.
  """

  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    return response.text
  except requests.exceptions.RequestException:
    return None


# Example usage
if __name__ == "__main__":
  url = "http://slowwly.robertomurray.co.uk"
  content = get_page(url)

  if content:
    print(f"Fetched content for {url}")
  else:
    print(f"Failed to fetch content for {url}")
