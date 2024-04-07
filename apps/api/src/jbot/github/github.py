import json
from jbot import config

from github import Github

# Authentication is defined via github.Auth
from github import Auth


class MyGithub:
    github: Github

    def __init__(self):
        pat = config.get_or_error("GITHUB_PERSONAL_ACCESS_TOKEN")
        # app_id = config.get_or_error("GITHUB_APP_ID")
        # private_key = config.get_or_error("GITHUB_PRIVATE_KEY")
        # installation_id = config.get_or_error("GITHUB_INSTALLATION_ID")
        # auth = Auth.AppAuth(app_id, private_key).get_installation_auth(
        #     int(installation_id)
        # )
        auth = Auth.Token(pat)
        self.github = Github(auth=auth)
        self.repo = self.github.get_repo(config.get("GITHUB_REPO"))
        print(self.repo.name)

    def search_code(self, query: str):
        github_search_query = f"{query} repo:{config.get('GITHUB_REPO')}"
        search_result = self.github.search_code(github_search_query).get_page(0)
        print(search_result[0].path, search_result[0].decoded_content)
        return search_result[0].decoded_content
