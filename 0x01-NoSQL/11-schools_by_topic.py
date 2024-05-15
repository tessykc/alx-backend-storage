#!/usr/bin/env python3
""" schools_by_topic """
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
  """Returns a list of school documents where the 'topics' field
  includes the provided topic.

  Args:
      mongo_collection (pymongo.collection.Collection): The pymongo
      collection object.
      topic (str): The topic to search for in the 'topics' field.

  Returns:
      list: A list of school documents matching the criteria.
  """

  # Filter to find documents with the topic in the 'topics' field
  # (using regex)
  filter = {"topics": {"$regex": topic, "$options": "i"}}  
  # Case-insensitive search

  # Find all documents matching the filter
  schools = mongo_collection.find(filter)

  # Return the list of school documents
  return list(schools)
