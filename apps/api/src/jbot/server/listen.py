import json
from pathlib import Path

from jbot.routers.linear import router as linear_router
from jbot.routers.github import router as github_router
from jbot.routers.llm import router as llm_router
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(linear_router)
app.include_router(github_router)
app.include_router(llm_router)


@app.get("/refresh-files")
def refresh_files():
    structure = files.get_folder_structure(Path(str(config.get("WORKSPACE_DIR"))))
    return json.dumps(structure.to_dict())


@app.get("/select-file")
def select_file(file: str):
    with open(Path(Path(str(config.get("WORKSPACE_DIR"))), file), "r") as selected_file:
        content = selected_file.read()
    return json.dumps({"code": content})
