from mongo_db_setup import categories_collection, db

def add_category(category_name, keywords=[]):
    if categories_collection.find_one({"name": category_name}):
        add_keywords_to_category(category_name,keywords)
        return get_keywords_by_category(category_name)
    else:
        categories_collection.insert_one({"name": category_name, "keywords": keywords})
        return keywords

def add_keywords_to_category(category_name, new_keywords):
    categories_collection.update_one({"name": category_name}, {"$addToSet": {"keywords": {"$each": new_keywords}}})


def get_keywords_by_category(category_name):
    category = categories_collection.find_one({"name": category_name}, {"_id": 0, "keywords": 1})
    if category:
        return category.get("keywords", [])
    else:
        return []

