from llama_index.core import SimpleDirectoryReader, Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore

from jbot import config


class MySupabaseVectorStore:
    def __init__(self):
        documents = SimpleDirectoryReader("./data/paul_graham/").load_data()

        connection_string = config.get_or_error("SUPABASE_DATABASE_URL")
        print(connection_string)

        vector_store = SupabaseVectorStore(
            postgres_connection_string=connection_string,
            collection_name="base_demo",
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )

    def query(self, query: str):
        query_engine = self.index.as_query_engine(similarity_top_k=2)
        response = query_engine.query(query)
        return response
