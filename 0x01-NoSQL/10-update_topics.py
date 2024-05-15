#!/usr/bin/env python3

from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
  """Updates the topics field of a school document based on the provided name and new topics list.

  Args:
      mongo_collection (pymongo.collection.Collection): The pymongo collection object.
      name (str): The name of the school document to update.
      topics (list): The list of new topics for the school.
  """

  # Filter to find the document by name
  filter = {"name": name}

  # Update operator to set the topics field
  update = {"$set": {"topics": topics}}

  # Update the document with the provided filter and update operator
  mongo_collection.update_one(filter, update)
