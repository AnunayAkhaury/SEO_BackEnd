from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from scraper import main

# Assuming your model functions are correctly imported
from models import add_category, add_keywords_to_category, get_keywords_by_category

app = FastAPI()


class CategoryURL(BaseModel):
    url: str

class KeywordsUpdate(BaseModel):
    keywords: List[str]
    
@app.post("/categories/", status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryURL):
    print(category_data.url)
    categories, keywords = main(category_data.url)
    print(categories)
    print(keywords)
    result_keywords = add_category(categories, keywords)
    return {
        "url": category_data.url,
        "categories": categories,
        "keywords": result_keywords
    }

@app.put("/categories/{category_name}/keywords/", status_code=status.HTTP_200_OK)
def update_keywords(category_name: str, keywords_update: KeywordsUpdate):
    add_keywords_to_category(category_name, keywords_update.keywords)
    return {"message": f"Keywords successfully added to {category_name}."}

@app.get("/categories/{category_name}/keywords/", status_code=status.HTTP_200_OK)
def read_keywords(category_name: str):
    keywords = get_keywords_by_category(category_name)
    if keywords is not None:
        return {"category": category_name, "keywords": keywords}
    else:
        raise HTTPException(status_code=404, detail="Category not found")