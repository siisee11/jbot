from jbot import config

from github import Github

# Authentication is defined via github.Auth
from github import Auth
from jbot.github.schemas.search_code import SearchCodeResultSchema


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

    def search_code(self, query: str) -> SearchCodeResultSchema | None:
        github_search_query = f"{query} repo:{config.get('GITHUB_REPO')}"
        search_result = self.github.search_code(
            github_search_query, highlight=True
        ).get_page(0)

        if not search_result:
            return None

        first_search_result = search_result[0]
        print(first_search_result.git_url)
        print(first_search_result.download_url)
        print(first_search_result.text_matches)
        print(first_search_result.name)

        search_result_dict = {
            "file_path": first_search_result.path,
            "content": first_search_result.decoded_content.decode("utf-8"),
            "fragment": first_search_result.text_matches[0]["fragment"],
        }

        return SearchCodeResultSchema.model_validate(search_result_dict)
