import requests


def getRepoLanguages(url: str):
    res = requests.get(url)
    if not res.ok:
        return False
    res = res.json()
    list_lang = []
    for x in res:
        list_lang.append(x)
    return list_lang
