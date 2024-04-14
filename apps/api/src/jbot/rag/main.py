from jbot.rag.core.index_builder.repo_index_builder import load_repo_index

from jbot.rag.embedder import Embedder
from jbot.vectorstore.weaviate import MyWeaviateVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core import Settings

from jbot import config

# global

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    api_key=config.get_or_error("OPENAI_API_KEY"),
)
Settings.embed_model = OpenAIEmbedding(
    api_key=config.get_or_error("OPENAI_API_KEY"),
    model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL,
)

embedder = Embedder(vectorstore=MyWeaviateVectorStore(index_name="RepoIndex"))
# embedder.embed() at first run
response = embedder.retrieve_results("How to run GetGPT?")
print(response)
