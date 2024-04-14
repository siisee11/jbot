from typing import List, Optional, Sequence

from pydantic import BaseModel


class Label(BaseModel):
    nodes: Optional[List[str]]


class Project(BaseModel):
    name: str


class State(BaseModel):
    name: str
    type: str


class Issue(BaseModel):
    id: str
    title: str
    description: str | None
    identifier: str
    labels: Label
    state: State
    project: Project
