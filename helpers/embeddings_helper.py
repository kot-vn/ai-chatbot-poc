import os

from collections import Counter
from constant_variables.configs import OPENAI_BASE_URL, OPENAI_EMBEDDINGS_MODEL
from django.db import connections
from langchain_openai import OpenAIEmbeddings
from typing import List, Tuple


class EmbeddingsHelper:
    def __init__(self) -> None:
        pass

    def generate_embeddings(self, openai_api_key, documents) -> List[float]:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        embeddings = OpenAIEmbeddings(
            check_embedding_ctx_length=False,
            base_url=OPENAI_BASE_URL,
            model=OPENAI_EMBEDDINGS_MODEL,
        )
        return embeddings.embed_query(documents)

    def get_top3_similar_collections(self, query: List[float]) -> List[Tuple[str]]:
        with connections["default"].cursor() as cursor:
            cursor.execute(
                "SELECT collection_id FROM knowledge",
            )

            collection_ids = cursor.fetchall()
            collection_ids = [item for sublist in collection_ids for item in sublist]
            format_strings = ",".join(["%s"] * len(collection_ids))

            cursor.execute(
                f"""
                SELECT collection_id
                FROM langchain_pg_embedding
                WHERE collection_id IN({format_strings})
                ORDER BY embedding <=> %s::vector
                LIMIT 3
                """,
                collection_ids + [query],
            )

            collection_ids = cursor.fetchall()
        return collection_ids

    def get_most_similar_collection(self, collection_ids: List[Tuple[str]]) -> str:
        collection_ids = [item for sublist in collection_ids for item in sublist]
        counter = Counter(collection_ids)
        most_common = counter.most_common(1)
        return most_common[0][0] if most_common else None
