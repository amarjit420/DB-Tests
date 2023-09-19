#!/usr/bin/env python3

import redis
import numpy as np
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

r = redis.Redis(host="127.0.0.1", port=6379)

INDEX_NAME = "index"                              # Vector Index Name
DOC_PREFIX = "doc:"                               # RediSearch Key Prefix for the Index

def create_index(vector_dimensions: int):
    try:
        print("!.")
        # check to see if index exists
        r.ft(INDEX_NAME)
        print("Index already exists!")
    except:
        # schema
        schema = (
            TagField("tag"),                       # Tag Field Name
            VectorField("vector",                  # Vector Field Name
                "FLAT", {                          # Vector Index Type: FLAT or HNSW
                    "TYPE": "FLOAT32",             # FLOAT32 or FLOAT64
                    "DIM": vector_dimensions,      # Number of Vector Dimensions
                    "DISTANCE_METRIC": "COSINE",   # Vector Search Distance Metric
                }
            ),
        )

        # index Definition
        definition = IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)

        # create Index
        r.ft(INDEX_NAME).create_index(fields=schema, definition=definition)

def redis_pipeline():
    # instantiate a redis pipeline
    pipe = r.pipeline()

    # define some dummy data
    objects = [
        {"name": "a", "tag": "foo"},
        {"name": "b", "tag": "foo"},
        {"name": "c", "tag": "bar"},
    ]

    # write data
    for obj in objects:
        # define key
        key = f"doc:{obj['name']}"
        # create a random "dummy" vector
        obj["vector"] = np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
        # HSET
        pipe.hset(key, mapping=obj)

    res = pipe.execute()

#KNN queries are for finding the topK most similar vectors given a query vector.
def redis_query():
    query = (
        Query("*=>[KNN 2 @vector $vec as score]")
            .sort_by("score")
            .return_fields("id", "score")
            .paging(0, 2)
            .dialect(2)
    )

    query_params = {
        "vec": np.random.rand(VECTOR_DIMENSIONS).astype(np.float32).tobytes()
    }
    r.ft(INDEX_NAME).search(query, query_params).docs


if __name__ == '__main__':
    # define vector dimensions
    VECTOR_DIMENSIONS = 1536

    # create the index
    create_index(vector_dimensions=VECTOR_DIMENSIONS)
    redis_pipeline()
    redis_query()
