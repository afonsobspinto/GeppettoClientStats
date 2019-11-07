from github import Github
import csv

from ComponentAnalysis import ComponentAnalysis
from settings import *
from utils import match_strings, is_javascript, get_type

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
    elif file_content.type != "dir" and (_type := get_type(file_content)) is not None \
            and is_javascript(file_content.path):
        try:
            components.append(ComponentAnalysis(file_content, component_factory, _type))
        except Exception as e:
            print("Warning " + str(e) + "\n" + file_content.path + ' skipped \n')

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
header = ['name', 'type', 'last_modified', 'usage', 'has_jquery', 'is_react', 'is_es6',
          'is_in_component_factory'] + USAGE_REPOS
header2 = ['', '', '', '', '', '', '', '']
for _ in USAGE_REPOS:
    header2 += ['imported/required', 'add_widget', 'add_component']
with f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(header2)
    for component in components:
        writer.writerow(component.get_row())
    print(OUTPUT_FILE + " created")
    f.close()
