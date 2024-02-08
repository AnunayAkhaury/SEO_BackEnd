from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os

def initialize_pinecone():
    load_dotenv()
    pc = Pinecone(os.getenv('PINECONE_API_KEY'))
    if "quickstart" not in pc.list_indexes():
        pc.create_index(
            name="quickstart",
            dimension=8,
            metric="euclidean",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-west-2'
            ) 
        )
    return pc.Index("quickstart")


def upsert_vectors(index, vectors, namespace):
    index.upsert(vectors=vectors, namespace=namespace)


def query_vectors(index, namespace, vector, top_k=3):
    return index.query(namespace=namespace, vector=vector, top_k=top_k, include_values=True)


# pc.create_index(
#     name="quickstart",
#     dimension=8,
#     metric="euclidean",
#     spec=ServerlessSpec(
#         cloud='aws', 
#         region='us-west-2'
#     ) 
# ) 

# index = pc.Index("quickstart")

# index.upsert(
#   vectors=[
#     {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
#     {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
#     {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
#     {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
#   ],
#   namespace="ns1"
# )

# index.upsert(
#   vectors=[
#     {"id": "vec5", "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]},
#     {"id": "vec6", "values": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]},
#     {"id": "vec7", "values": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
#     {"id": "vec8", "values": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}
#   ],
#   namespace="ns2"
# )

# index.describe_index_stats()

# index.query(
#   namespace="ns1",
#   vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
#   top_k=3,
#   include_values=True
# )

# index.query(
#   namespace="ns2",
#   vector=[0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
#   top_k=3,
#   include_values=True
# )