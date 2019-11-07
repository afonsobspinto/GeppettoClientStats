import github
from github import Consts
import re

from settings import COMPONENTS_FOLDER_AUX


def match_strings(s1, s2):
    return s1 in s2 or s2 in s1


def is_javascript(s):
    return s.endswith('.js') or s.endswith('.ts') or s.endswith('.tsx') or s.endswith('.jsx')


def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None


def last_modified_fix(content):
    if isinstance(content, github.ContentFile.ContentFile):
        commits = content.repository.get_commits(path=content.path)
        most_recent_commit = commits[0]
        date = most_recent_commit.commit.author.date
    else:
        date = content._headers.get(Consts.RES_LAST_MODIFIED)
    return date


def get_type(file_content):
    for i in COMPONENTS_FOLDER_AUX:
        if i in file_content.path:
            return i
    return None
