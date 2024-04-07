from jbot import config

from github import Github

# Authentication is defined via github.Auth
from github import Auth


class MyGithub:
    def __init__(self):
        app_id = config.get_or_error("GITHUB_APP_ID")
        private_key = config.get_or_error("GITHUB_PRIVATE_KEY")
        installation_id = config.get_or_error("GITHUB_INSTALLATION_ID")
        auth = Auth.AppAuth(app_id, private_key).get_installation_auth(
            int(installation_id)
        )
        self.github = Github(auth=auth)
        self.repo = self.github.get_repo(config.get("GITHUB_REPO"))
        print(self.repo.name)
        pass
