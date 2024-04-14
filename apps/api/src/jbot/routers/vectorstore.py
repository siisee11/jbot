from fastapi import APIRouter
from jbot.rag.embedder import Embedder
from jbot.vectorstore.supabase import MySupabaseVectorStore
from jbot.vectorstore.weaviate import MyWeaviateVectorStore
from opendevin.agent import Agent
from jbot import config


router = APIRouter(
    prefix="/vectorstore",
)

weaviate = MyWeaviateVectorStore()
supabase = MySupabaseVectorStore()


embedder = Embedder(vectorstore=MyWeaviateVectorStore(index_name="RepoIndex"))


@router.post("/weaviate/query")
async def query(query: str):
    """
    Query to Weaviate vector store.
    """
    # return weaviate.query(query)
    return embedder.retrieve_results(query)


@router.post("/supabase/query")
async def query(query: str):
    """
    Query to Supabase vector store.
    """
    return supabase.query(query)


@router.get("/agents")
async def get_litellm_agents():
    """
    Get all agents supported by LiteLLM.
    """
    try:
        return Agent.listAgents()
    except ValueError:
        return "No agent class registered."


@router.get("/default-model")
def read_default_model():
    return config.get_or_error("LLM_MODEL")
