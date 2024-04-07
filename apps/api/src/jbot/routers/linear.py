from fastapi import APIRouter
from jbot.linear.linear import Linear


router = APIRouter(
    prefix="/linear",
)

linear = Linear()


@router.get("/me")
def get_me():
    return linear.get_me()


@router.get("/me/issues")
def get_my_issues():
    return linear.get_my_issues()


@router.get("/teams")
def get_teams():
    return linear.get_teams()


@router.post("/issue")
def create_issue(title: str, description: str):
    return linear.create_issue(title, description)
