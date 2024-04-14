from typing import List
import weaviate
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from jbot import config


class MyWeaviateVectorStore:
    def __init__(self, index_name="LlamaIndex"):
        self.index = None
        self.index_name = index_name
        self.client = weaviate.Client(
            url="http://localhost:8080",
            additional_headers={
                "X-OpenAI-Api-Key": config.get_or_error("OPENAI_API_KEY")
            },
        )

        if index_name == "LlamaIndex":
            documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
            vector_store = WeaviateVectorStore(
                weaviate_client=self.client, index_name=self.index_name
            )
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self.index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )

        vector_store = WeaviateVectorStore(
            weaviate_client=self.client, index_name=self.index_name
        )
        self.index = VectorStoreIndex.from_vector_store(vector_store)

    def load(self):
        if self.index is None:
            raise ValueError("Index not found")
        return self.index

    def add_documents(self, documents: List[Document]):
        vector_store = WeaviateVectorStore(
            weaviate_client=self.client, index_name=self.index_name
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )

    def query(self, query: str):
        if self.index is None:
            raise ValueError("Index not found")
        query_engine = self.index.as_query_engine(similarity_top_k=2)
        response = query_engine.query(query)
        return response
