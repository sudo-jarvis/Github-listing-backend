import requests


def getRepoLanguages(url: str):
    res = requests.get(url)
    if not res.ok:
        return False
    return res.json()
