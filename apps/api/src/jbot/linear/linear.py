import json
from typing import Optional, Union
from jbot import config
import requests


class Linear:
    def __init__(self, url: str = "https://api.linear.app/graphql"):
        self.apikey = config.get_or_error("LINEAR_API_KEY")
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.apikey,
        }
        teams_data = self.get_teams()
        teams = teams_data["data"]["teams"]["nodes"]
        team = next(
            filter(
                lambda t: t["name"] == config.get("LINEAR_WORKSPACE_NAME"),
                teams,
            ),
            None,
        )
        self.team = team

        me_data = self.get_me()
        self.me = me_data["data"]["viewer"]

    def _query(self, query: str, variables: Optional[dict] = None) -> dict:
        """
        Make query response
        """
        response = requests.post(
            url=self.url,
            json={"query": query, "variables": variables},
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "Query failed to run by returning code of {}. {}".format(
                    response.status_code, response.text
                )
            )

    def get_me(self):
        query = """
        { viewer { id name email } }
        """
        data = self._query(query)
        return data

    def get_my_todo_issues(self, first: int = 1):
        query = """
        query User($userId: String!, $first: Int, $filter: IssueFilter) {
            user(id: $userId) {
                assignedIssues(first: $first, filter: $filter) {
                    nodes {
                        id
                        title
                        description
                        identifier
                        labels {
                            nodes {
                                name
                            }
                        }
                        state {
                            name
                            type
                        }
                        project {
                            name
                        }
                    }
                }
            }
        }
        """
        variables = {
            "userId": self.me["id"],
            "first": first,
            "filter": {"state": {"type": {"eq": "unstarted"}}},
        }
        data = self._query(query, variables)
        return data

    def get_teams(self):
        # TODO: Type the return value
        query = """
        { teams { nodes { id name } } }
        """
        data = self._query(query)
        return data

    def create_issue(self, title: str, description: str):
        query = """
        mutation IssueCreate($input: IssueCreateInput!) {
        issueCreate(
            input: $input
        ) {
            success
            issue {
                id
                title
            }
        }
        }
        """
        variables = {
            "input": {
                "title": title,
                "description": description,
                "teamId": self.team["id"],
            }
        }

        data = self._query(query, variables)
        return data
