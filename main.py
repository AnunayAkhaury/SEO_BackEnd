from typing import Union
from fastapi import FastAPI
from pinecone_database import initialize_pinecone, upsert_vectors, query_vectors

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

index = initialize_pinecone()  

@app.on_event("startup")
async def startup_event():
    vectors_ns1 = [
        {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
        {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
        {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
        {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]},
    ]
    upsert_vectors(index, vectors_ns1, "ns1")

@app.get("/query/")
async def query_vector(namespace: str, vector: list[float]):
    results = query_vectors(index, namespace, vector)
    return {"results": results}