from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType

from jbot import config

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    api_key=config.get_or_error("OPENAI_API_KEY"),
)
Settings.embed_model = OpenAIEmbedding(
    api_key=config.get_or_error("OPENAI_API_KEY"),
    model=OpenAIEmbeddingModelType.TEXT_EMBED_3_SMALL,
)
