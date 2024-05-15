#!/usr/bin/env python3
""" log-stats """

from pymongo import MongoClient


def count_logs(collection):
  """Counts the total number of documents in the collection.

  Args:
      collection (pymongo.collection.Collection): The pymongo 
      collection object.

  Returns:
      int: The total number of documents in the collection.
  """

  return collection.count_documents({})


""" count method """
def count_method(collection, method):
  """Counts the number of documents with a specific method field 
  value.

  Args:
      collection (pymongo.collection.Collection): The pymongo 
      collection object.
      method (str): The method value to search for.

  Returns:
      int: The number of documents with the specified method.
  """

  filter = {"method": method}
  return collection.count_documents(filter)


""" count status check """
def count_status_check(collection):
  """Counts the number of documents where the path is "/status".

  Args:
      collection (pymongo.collection.Collection): The pymongo 
      collection object.

  Returns:
      int: The number of documents with the "/status" path.
  """

  filter = {"path": "/status"}
  return collection.count_documents(filter)


""" top_ips """
def top_ips(collection, limit=10):
  """Finds the top 'limit' most frequent IP addresses in the 
  collection.

  Args:
      collection (pymongo.collection.Collection): The pymongo 
      collection object.
      limit (int, optional): The maximum number of IPs to return (default: 10).

  Returns:
      list: A list of dictionaries with 'ip' and 'count' keys 
      for each top IP.
  """

  # Use aggregation to group by IP and count documents
  pipeline = [
      {
          "$group": {
              "_id": "$remote_addr",  # Group by IP address
              "count": { "$sum": 1 }   # Count documents in each group
          }
      },
      {
          "$sort": { "count": -1 }  # Sort by count (descending)
      },
      {
          "$limit": limit  # Limit the number of results
      }
  ]

  # Execute the pipeline and convert results to a list
  results = list(collection.aggregate(pipeline))

  # Add 'ip' key to each document
  for item in results:
    item["ip"] = item["_id"]
    del item["_id"]  # Remove temporary group ID

  return results


""" main """
def main():
  """Connects to MongoDB, retrieves data, and displays statistics."""

  # Connect to MongoDB
  client = MongoClient("mongodb://localhost:27017/")
  db = client["logs"]  # Replace with your database name
  collection = db["nginx"]  # Replace with your collection name

  # Count total logs
  total_logs = count_logs(collection)

  # Count methods
  methods = {
      "GET": count_method(collection, "GET"),
      "POST": count_method(collection, "POST"),
      "PUT": count_method(collection, "PUT"),
      "PATCH": count_method(collection, "PATCH"),
      "DELETE": count_method(collection, "DELETE"),
  }

  # Count status checks
  status_checks = count_status_check(collection)

  # Print statistics
  print(f"{total_logs} logs")
  print("Methods:")
  for method, count in methods.items():
    print(f"\tmethod {method}: {count}")
  print(f"{status_checks} status check")

if __name__ == "__main__":
  main()
