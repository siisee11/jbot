from fastapi import APIRouter
from jbot.github.github import MyGithub


router = APIRouter(
    prefix="/github",
)

github = MyGithub()


@router.get("/repo-name")
def get_repo_name():
    return github.repo.name


@router.get("/search-code")
def search_code(query: str):
    return github.search_code(query)
