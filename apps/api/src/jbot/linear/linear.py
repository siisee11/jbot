import json
from typing import Union
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
        data = self.get_teams()
        teams = data["data"]["teams"]["nodes"]
        team = next(filter(lambda t: t["name"] == "Wordbricks", teams), None)
        self.team = team

    def _query(self, query: str) -> Union[str, dict]:
        response = requests.post(
            url=self.url, json={"query": query}, headers=self.headers
        )
        if response.status_code == 200:
            return response.json()

        return response.content

    def _mutate(self, query: str, variables: dict) -> Union[str, dict]:
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

    def get_issues(self):
        query = """
        { issues { nodes { id title } } }
        """
        data = self._query(query)
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

        data = self._mutate(query, variables)
        return data
