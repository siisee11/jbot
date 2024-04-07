from fastapi import APIRouter
import litellm
from opendevin.agent import Agent
from jbot import config


router = APIRouter(
    prefix="/llm",
)


@router.get("/models")
async def get_litellm_models():
    """
    Get all models supported by LiteLLM.
    """
    return list(set(litellm.model_list + list(litellm.model_cost.keys())))


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
