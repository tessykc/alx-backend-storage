#!/usr/bin/env python3

from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
  """Inserts a new document into the provided collection and returns the inserted document's _id.

  Args:
      mongo_collection (pymongo.collection.Collection): The pymongo collection object.
      **kwargs: Keyword arguments representing the document fields and their values.

  Returns:
      ObjectId: The ObjectId of the inserted document.
  """

  # Create the document dictionary from kwargs
  document = {key: value for key, value in kwargs.items()}

  # Insert the document and get the result
  result = mongo_collection.insert_one(document)

  # Return the inserted document's _id
  return result.inserted_id
