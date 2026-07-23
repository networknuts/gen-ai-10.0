from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client['checkpointing_db']

collections = db.list_collection_names()

for collection_name in collections:
    print(f"COLLECTION: {collection_name}")
    collection = db[collection_name]
    documents = collection.find()
    for doc in documents:
        print(doc)