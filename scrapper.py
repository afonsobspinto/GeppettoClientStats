from github import Github
from settings import *
from utils import match_strings


# Create a Github instance:
g = Github(GITHUB_ACCESS_TOKEN)

# Get repo to analyse
repo = g.get_repo(REPO)
print(repo.name)
print('\n')

# Get all of the contents of the repository recursively
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir" and any([match_strings(file_content.path, i) for i in COMPONENTS_FOLDER_PATH]):
        contents.extend(repo.get_contents(file_content.path))
    elif any([i in file_content.path for i in COMPONENTS_FOLDER_AUX]):
        # Go over usage repos
        print(file_content)
        # for r_name in USAGE_REPOS:
        #     r = g.get_repo(r_name)
        #     print(r.name)
print('\n')



