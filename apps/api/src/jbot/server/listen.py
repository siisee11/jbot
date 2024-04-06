import json
import uuid
from pathlib import Path

from jbot.linear.linear import Linear
import litellm
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from jbot import config, files
from opendevin.agent import Agent

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security_scheme = HTTPBearer()

# This endpoint receives events from the client (i.e. the browser)
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     sid = get_sid_from_token(websocket.query_params.get("token") or "")
#     if sid == "":
#         return
#     session_manager.add_session(sid, websocket)
#     # TODO: actually the agent_manager is created for each websocket connection, even if the session id is the same,
#     # we need to manage the agent in memory for reconnecting the same session id to the same agent
#     agent_manager = AgentManager(sid)
#     await session_manager.loop_recv(sid, agent_manager.dispatch)


@app.get("/litellm-models")
async def get_litellm_models():
    """
    Get all models supported by LiteLLM.
    """
    return list(set(litellm.model_list + list(litellm.model_cost.keys())))


@app.get("/litellm-agents")
async def get_litellm_agents():
    """
    Get all agents supported by LiteLLM.
    """
    try:
        return Agent.listAgents()
    except ValueError:
        return "No agent class registered."


@app.get("/default-model")
def read_default_model():
    return config.get_or_error("LLM_MODEL")


@app.get("/refresh-files")
def refresh_files():
    structure = files.get_folder_structure(Path(str(config.get("WORKSPACE_DIR"))))
    return json.dumps(structure.to_dict())


@app.get("/select-file")
def select_file(file: str):
    with open(Path(Path(str(config.get("WORKSPACE_DIR"))), file), "r") as selected_file:
        content = selected_file.read()
    return json.dumps({"code": content})


@app.get("/linear/issues")
def get_linear_issues():
    linear = Linear()
    issues = linear.get_issues()
    return json.dumps(issues)
