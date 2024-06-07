import requests
# from langchain_community.tools.github.tool import GitHubAction
from langchain_core.tools import tool

from config import GITHUB_ACCESS_TOKEN, GITHUB_REPOSITORY

# too = github
@tool
def GitHubAction(repo_address, github_token):
    """This gets the logs of last 30 commits done in a github repository"""
    headers = {
        "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"https://api.github.com/repos/{GITHUB_REPOSITORY}/commits", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
