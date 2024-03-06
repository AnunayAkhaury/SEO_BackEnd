from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb://localhost:27017"


client = MongoClient(uri, server_api=ServerApi('1'))

db_names = client.list_database_names()
if "SEO2024" in db_names:
    print("Successfully connected to the SEO2024 database.")
else:
    print("Failed to connect to the SEO2024 database.")

db = client['SEO2024']
collection_names = db.list_collection_names()
if "Industy/Keywords" in collection_names:
    print("Successfully connected to the Industy/Keywords collection.")
else:
    print("Failed to connect to the Industy/Keywords collection.")

test_data = {"test": "data"}
categories_collection = db["Industy/Keywords"]
categories_collection.insert_one(test_data)

retrieved_data = db["Industy/Keywords"].find_one({"test": "data"})
if retrieved_data:
    print("Successfully inserted and retrieved data from Industy/Keywords collection:", retrieved_data)
else:
    print("Failed to insert or retrieve data from Industy/Keywords collection.")
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
