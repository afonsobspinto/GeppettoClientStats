import re
from enum import Enum

from settings import USAGE_MAP, USAGE_REPOS


class Usage(Enum):
    IMPORT = 0
    ADD_WIDGET = 1
    ADD_COMPONENT = 2


class UsageAnalysis:
    ADD_WIDGET = "G.addWidget"

    def __init__(self, name):
        self.name = name
        pass

    def _check_imports(self, file_content, file_path, repo_name):
        is_used = self.name.split('.')[0] in file_content
        if is_used:
            self._add_usage(Usage.IMPORT, file_path, repo_name)

    def _check_add_widget(self, file_content, file_path, repo_name):
        add_widget_entries = re.findall(rf"{self.ADD_WIDGET}\((.*),",file_content)
        for entry in add_widget_entries:
            if entry in USAGE_MAP.keys():
                if USAGE_MAP[entry] in self.name:
                    self._add_usage(Usage.ADD_WIDGET, file_path, repo_name)

    def _add_usage(self, usage, file_path, repo_name):
        attr = getattr(self, repo_name)
        if attr == 0:
            setattr(self, repo_name, [[], [], []])
            attr = getattr(self, repo_name)
        attr[usage.value].append(file_path)

    def check_usage(self, file_content, file_path, repo_name):
        if not hasattr(self, repo_name):
            setattr(self, repo_name, 0)
        self._check_imports(file_content, file_path, repo_name)
        self._check_add_widget(file_content, file_path, repo_name)

    def get_row(self):
        row = []
        for r_name in USAGE_REPOS:
            usages = getattr(self, r_name)
            if usages != 0:
                for usage in usages:
                    row += usage
        return row

