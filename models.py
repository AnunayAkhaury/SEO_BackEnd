
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017"


client = MongoClient(uri, server_api=ServerApi('1'))



def check_category(category_name):
    db = client['SEO2024']
    categories_collection = db["Industy/Keywords"]
    if categories_collection.find_one({"name": category_name}):
        print("Category already exists. Adding keywords.")
        print("CATEGORY EXISTS")
        return get_keywords_by_category(category_name)
    return None
    
def add_category(category_name, keywords=[]):
    db = client['SEO2024']
    categories_collection = db["Industy/Keywords"]
    if categories_collection.find_one({"name": category_name}):
        # print("Category already exists. Adding keywords.")
        add_keywords_to_category(category_name, keywords)
        return get_keywords_by_category(category_name)
    else:
        result = categories_collection.insert_one({"name": category_name, "keywords": keywords})
        if result.inserted_id:
            print("Category added with keywords:", keywords)
            return keywords
        else:
            print("Failed to add category.")
            return []


def add_keywords_to_category(category_name, new_keywords):
    uri = "mongodb://localhost:27017"


    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['SEO2024']
    categories_collection = db["Industy/Keywords"]
    categories_collection.update_one({"name": category_name}, {"$addToSet": {"keywords": {"$each": new_keywords}}})


def get_keywords_by_category(category_name):
    uri = "mongodb://localhost:27017"


    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['SEO2024']
    categories_collection = db["Industy/Keywords"]
    category = categories_collection.find_one({"name": category_name}, {"_id": 0, "keywords": 1})
    if category:
        return category.get("keywords", [])
    else:
        return []

