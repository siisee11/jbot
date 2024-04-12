import weaviate
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import StorageContext
from jbot import config


class MyWeaviateVectorStore:
    def __init__(self):
        self.client = weaviate.Client(
            url="http://localhost:8080",
            additional_headers={
                "X-OpenAI-Api-Key": config.get_or_error("OPENAI_API_KEY")
            },
        )

        documents = SimpleDirectoryReader("./data/paul_graham/").load_data()

        vector_store = WeaviateVectorStore(weaviate_client=self.client)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )

    def query(self, query: str):
        query_engine = self.index.as_query_engine(similarity_top_k=2)
        response = query_engine.query(query)
        return response
