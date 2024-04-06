from jbot import config
import requests


class Linear:
    apikey: str
    headers: dict

    def __init__(self, url: str = "https://api.linear.app/graphql"):
        self.apikey = config.get_or_error("LINEAR_API_KEY")
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.apikey,
        }
        print("self.headers : ", self.headers)

    def get_issues(self):
        query = """
        { issues { nodes { id title } } }
        """
        response = requests.post(
            url=self.url, json={"query": query}, headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
