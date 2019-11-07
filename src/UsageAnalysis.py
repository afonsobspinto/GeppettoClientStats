import re
from enum import Enum

from src.settings import USAGE_MAP, USAGE_REPOS


class Usage(Enum):
    IMPORT = 0
    ADD_WIDGET = 1
    ADD_COMPONENT = 2


class UsageAnalysis:
    ADD_WIDGET = "G.addWidget"
    ADD_COMPONENT = "GEPPETTO.ComponentFactory.addComponent"

    def __init__(self, name):
        self.name = name
        self.total_usage = 0
        self.repos_usage = set()
        pass

    def _check_relative_imports(self, file_content, file_path, repo_name):
        is_used = re.findall(rf"import.*from.*\..*/{self.name.split('.')[0].split('/')[-2]}/{self.name.split('.')[0].split('/')[-1]}'",file_content)
        if is_used:
            self._add_usage(Usage.IMPORT, file_path, repo_name)

    def _check_relative_requires(self, file_content, file_path, repo_name):
        is_used = re.findall(rf"require\(.*\..*/{self.name.split('.')[0].split('/')[-2]}/{self.name.split('.')[0].split('/')[-1]}'\)",file_content)
        if is_used :
            self._add_usage(Usage.IMPORT, file_path, repo_name)

    def _check_absolute_imports(self, file_content, file_path, repo_name):
        is_used = re.findall(rf"{self.name.split('.')[0]}('|\.)",file_content)
        if is_used:
            self._add_usage(Usage.IMPORT, file_path, repo_name)

    def _check_add_component(self, file_content, file_path, repo_name):
        add_component_entries = re.findall(rf"{self.ADD_COMPONENT}\('(.*) *',",file_content)
        for entry in add_component_entries:
            if entry in USAGE_MAP.keys():
                if USAGE_MAP[entry] in self.name:
                    self._add_usage(Usage.ADD_COMPONENT, file_path, repo_name)

    def _check_add_widget(self, file_content, file_path, repo_name):
        add_widget_entries = re.findall(rf"{self.ADD_WIDGET}\((.*),",file_content)
        for entry in add_widget_entries:
            if entry in USAGE_MAP.keys():
                if USAGE_MAP[entry] in self.name:
                    self._add_usage(Usage.ADD_WIDGET, file_path, repo_name)

    def _add_usage(self, usage, file_path, repo_name):
        attr = getattr(self, repo_name)
        if attr == 0:
            setattr(self, repo_name, [set(), set(), set()])
            attr = getattr(self, repo_name)
        if file_path not in attr[usage.value]:
            attr[usage.value].add(file_path)
            self.total_usage += 1
            self.repos_usage.add(repo_name)

    def check_usage(self, file_content, file_path, repo_name):
        if not hasattr(self, repo_name):
            setattr(self, repo_name, 0)
        self._check_relative_imports(file_content, file_path, repo_name)
        self._check_relative_requires(file_content, file_path, repo_name)
        self._check_absolute_imports(file_content, file_path, repo_name)
        self._check_add_widget(file_content, file_path, repo_name)
        self._check_add_component(file_content, file_path, repo_name)

    def get_row(self):
        outter = []
        for usage_repo in USAGE_REPOS:
            inner = []
            usages = getattr(self, usage_repo[0])
            if usages != 0:
                for u in usages:
                    if len(u) == 0:
                        inner.append({0})
                    else:
                        inner.append(u)
            else:
                for i in range(3):
                    inner.append({0})
            outter.append(inner)
        return outter

    def get_total_usage(self):
        return self.total_usage

    def get_total_applications_usage(self):
        return len(self.repos_usage)