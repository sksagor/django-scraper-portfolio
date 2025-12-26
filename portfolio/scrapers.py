import requests
from django.conf import settings

GITHUB_API_BASE = "https://api.github.com"

def fetch_github_repo_metadata(owner: str, repo: str, token: str | None = None) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "language": data.get("language"),
        "license": data.get("license", {}).get("name") if data.get("license") else None,
        "html_url": data.get("html_url"),
    }