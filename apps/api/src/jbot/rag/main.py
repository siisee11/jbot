from jbot.rag.core.index_builder.repo_index_builder import load_repo_index

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

repo_index = load_repo_index()
query_engine = repo_index.as_query_engine()
response = query_engine.query("Who is the author?")
print(response)
