from typing import List
from pydantic import BaseModel

from src.jbot.linear.schema.issue import Issue


class AssignedIssues(BaseModel):
    # Define the structure of the 'assignedIssues' object
    nodes: List[Issue]


class UserData(BaseModel):
    # Define the structure of the 'user' object
    assignedIssues: AssignedIssues


class GetMyTodoIssuesData(BaseModel):
    # Define the structure of the 'data' object
    user: UserData


class GetMyTodoIssuesResponse(BaseModel):
    # Define the structure of the JSON response
    data: GetMyTodoIssuesData
