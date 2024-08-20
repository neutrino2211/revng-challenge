import collections.abc
import json
import enum
import typing
import requests

Commit = typing.Dict[str, typing.Any]

class AuthMethod(enum.Enum):
  PERSONAL_ACCESS_TOKEN = 1
  OAUTH_FLOW = 2

def get_commits(method: AuthMethod, token: str) -> typing.List[Commit]:
  repo = input("Repository: ")
  owner = input("Owner: ")
  if method == AuthMethod.PERSONAL_ACCESS_TOKEN:
    res = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits", headers={'Authorization': token})
    commits_array = res.json()

    assert isinstance(commits_array, collections.abc.Sequence), "Invalid response:\n" + json.dumps(commits_array)

    return commits_array
  elif method == AuthMethod.OAUTH_FLOW: # Not implemented due to time constraints
    return []