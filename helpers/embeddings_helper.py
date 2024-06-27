import os

from constant_variables.configs import OPENAI_BASE_URL, OPENAI_EMBEDDINGS_MODEL
from langchain_openai import OpenAIEmbeddings
from typing import List


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
