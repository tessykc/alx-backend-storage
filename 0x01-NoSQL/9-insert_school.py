#!/usr/bin/env python3

from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection based on keyword arguments.

    Args:
        mongo_collection: A pymongo collection object.
        **kwargs: Keyword arguments representing the fields and values for the new document.

    Returns:
        The new _id of the inserted document.
    """
    try:
        result = mongo_collection.insert_one(kwargs)
        return result.inserted_id
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    new_school_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    # List all documents in the collection
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('address', "")))
