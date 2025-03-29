import json

import urllib3


def get_latest_commit_hash(token: str, repo: str, branch: str = "main") -> str:
    url = f"https://api.github.com/repos/{repo}/commits/{branch}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    http = urllib3.PoolManager()
    res = http.request(
        method="GET",
        url=url,
        headers=headers,
    )

    if res.status != 200:
        raise Exception(f'Failed to request "GET {url}". status: {res.status}') from None

    data = json.loads(res.data.decode())

    return data["sha"]
