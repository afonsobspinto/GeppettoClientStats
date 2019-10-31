from github import Github
import csv

from ComponentAnalysis import ComponentAnalysis
from settings import *
from utils import match_strings, is_javascript

# Create a Github instance:
g = Github(GITHUB_ACCESS_TOKEN)

# Get repo to analyse
repo = g.get_repo(REPO)

# Get all of the contents of the repository recursively
components = []
component_factory = repo.get_contents('/js/components/ComponentFactory.js').decoded_content.decode("utf-8")
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir" and any([match_strings(file_content.path, i) for i in COMPONENTS_FOLDER_PATH]):
        contents.extend(repo.get_contents(file_content.path))
    elif file_content.type != "dir" and any([i in file_content.path for i in COMPONENTS_FOLDER_AUX])\
            and is_javascript(file_content.path):
        components.append(ComponentAnalysis(file_content, component_factory))

# Go over usage repos
for r_name in USAGE_REPOS:
    r = g.get_repo(r_name)
    contents = r.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(r.get_contents(file_content.path))
        elif is_javascript(file_content.path):
            decoded_content = None
            try:
                decoded_content = file_content.decoded_content.decode("utf-8")
            except Exception as e:
                print("Error " + str(e) + " " + file_content.path + '\n')
            for component in components:
                component.check_usage(decoded_content, file_content.path, r_name)

f = open(OUTPUT_FILE, 'w')
header = ['name'] + [a for a in dir(components[0]) if not a.startswith('__') and
          not a == 'name' and not a.endswith('Lookup')
          and not callable(getattr(components[0], a))]
with f:
    writer = csv.writer(f)
    writer.writerow(header)
    for component in components:
        writer.writerow([component.name] + [getattr(component, a) for a in dir(component) if not a.startswith('__') and
                         not a == 'name' and not a.endswith('Lookup')
                         and not callable(getattr(component, a))])
    print(OUTPUT_FILE + " created")
    f.close()


