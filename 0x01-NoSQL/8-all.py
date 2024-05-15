from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in the specified MongoDB collection.

    Args:
        mongo_collection: A pymongo collection object.

    Returns:
        A list of documents (dictionaries) from the collection.
    """
    try:
        return list(mongo_collection.find())
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage:
if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)

    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
