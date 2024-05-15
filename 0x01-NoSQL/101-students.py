#!/usr/bin/env python3
""" students """
from pymongo import MongoClient
from operator import itemgetter


def top_students(mongo_collection):
  """Calculates the average score for each student and returns 
  them sorted by average score in descending order.

  Args:
      mongo_collection (pymongo.collection.Collection): The pymongo
      collection object containing student documents.

  Returns:
      list: A list of dictionaries representing students with an 
      additional 'averageScore' key. The list is sorted by 'averageScore' in descending order.
  """

  # Aggregate pipeline to calculate average score
  pipeline = [
      {
          "$unwind": "$topics"  
        # Deconstruct topics array into separate documents
      },
      {
          "$group": {
              "_id": "$_id",  # Group by student ID
              "name": { "$first": "$name" },  
            # Get the first name from the group
              "topics": { "$push": "$topics" },  
            # Accumulate topics for each student
              "averageScore": { "$avg": "$topics.score" } 
            # Calculate average score
          }
      },
      {
          "$sort": { "averageScore": -1 }  
        # Sort by average score (descending)
      }
  ]

  # Execute the aggregation pipeline
  students = list(mongo_collection.aggregate(pipeline))

  return students
