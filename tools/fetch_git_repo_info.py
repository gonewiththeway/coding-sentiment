import requests
from langchain_core.tools import tool

@tool
def fetch_git_repo_info(repo_address, github_token):
    """This gets the logs of last 30 commits done in a git repository"""
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"https://api.github.com/repos/{repo_address}/commits", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
