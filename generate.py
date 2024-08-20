from commits import get_commits, AuthMethod, Commit
from graph import Graph
from typing import List
from os import environ

import pydot

ACCESS_TOKEN = environ.get("GITHUB_ACCESS_TOKEN")

commits = get_commits(AuthMethod.PERSONAL_ACCESS_TOKEN, ACCESS_TOKEN)

def generate_graphviz(name: str, commits: List[Commit]) -> str:
  content = '''
digraph {0} {{
 fontname="Helvetica,Arial,sans-serif"
 node [fontname="Helvetica,Arial,sans-serif"]
 edge [fontname="Helvetica,Arial,sans-serif"]
'''.format(name)
  
  for commit in commits:
    commit_message = commit['commit']['message'].replace("\n", " ").replace("\"", "'")
    content += f" n{commit['sha']} [label=\"{commit['sha']}\" URL=\"{commit['url']}\" tooltip=\"{commit_message}\"];\n"

  for commit in commits:
    for p in commit['parents']:
      content += f" n{p['sha']} -> n{commit['sha']};\n"

  content += "}"

  return content.strip()

def is_acyclic(commits: List[Commit]) -> bool:
  g = Graph(len(commits))

  indices_dict = {}

  for i, commit in enumerate(commits):
    indices_dict[commit['sha']] = i
  
  for commit in commits:
    for p in commit['parents']:
      if p['sha'] in indices_dict:
        g.addEdge(indices_dict[commit['sha']], indices_dict[p['sha']])

  return g.topologicalSort()

# commits[-1]['parents'].append({'sha': commits[0]['sha'], 'url': commits[0]['url'], 'html_url': commits[0]['html_url']})

r_commits = commits
r_commits.reverse()
assert is_acyclic(r_commits), "Commits are cyclic"

content = generate_graphviz("commits", commits)

with open('out.dot', 'w') as dotfile:
  dotfile.write(content)

graph, = pydot.graph_from_dot_file('out.dot')

graph.write_png("output.png")