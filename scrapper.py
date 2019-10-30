from github import Github

from ComponentAnalysis import ComponentAnalysis
from settings import *
from utils import match_strings, is_javascript

# Create a Github instance:
g = Github(GITHUB_ACCESS_TOKEN)

# Get repo to analyse
repo = g.get_repo(REPO)

# Get all of the contents of the repository recursively
components = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir" and any([match_strings(file_content.path, i) for i in COMPONENTS_FOLDER_PATH]):
        contents.extend(repo.get_contents(file_content.path))
    elif file_content.type != "dir" and any([i in file_content.path for i in COMPONENTS_FOLDER_AUX])\
            and is_javascript(file_content.path):
        # Go over usage repos
        components.append(ComponentAnalysis(file_content.path))

        # for r_name in USAGE_REPOS:
        #     r = g.get_repo(r_name)
        #     print(r.name)

for component in components:
    print(component)

