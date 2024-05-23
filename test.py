from urllib.parse import quote

import requests

projects = [
    {
        "name": "北汽福田",
        "url": "https://apitable.daocloud.io/share/shrW30wlzMG0WjXn0ezuN"
    }
]


def call_api(url: str, name: str):
    url = f"http://127.0.0.1:8000/test-record?folder_url={quote(url, safe='')}&folder_name={name}"
    print(url)
    resp = requests.post(url=url, headers={"Content-Type": "application/json"})
    print(name, resp.status_code, resp.text)


if __name__ == '__main__':
    for project in projects:
        if project["url"] and project["name"]:
            call_api(project["url"], project["name"])
