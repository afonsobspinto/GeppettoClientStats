from settings import USAGE_REPOS
from utils import last_modified_fix, is_phrase_in, is_javascript


class ComponentAnalysis:
    jqueryLookup = ['$', 'jQuery']
    reactLookup = ['react', 'componentWillMount', 'componentDidMount', 'shouldComponentUpdate', 'componentWillUpdate',
                   'componentDidUpdate', 'componentWillReceiveProps', 'shouldComponentUpdate',
                   'componentWillUpdate', 'componentDidUpdate', 'componentWillUnmount']
    es6Lookup = ['=>', 'let', 'const']

    def __init__(self, content, component_factory, usage_repos):
        self.name = content.path
        self.last_modified = last_modified_fix(content)
        decoded_content = None
        try:
            decoded_content = content.decoded_content.decode("utf-8")
        except Exception as e:
            print("Error " + str(e) + "\n" + self.name + ' skipped \n')

        if decoded_content:
            self.has_jquery = self.has_jquery(decoded_content)
            self.is_react = self.is_react(decoded_content)
            self.is_es6 = self.is_es6(decoded_content)
        self.is_in_component_factory = self.is_in_component_factory(component_factory)

        # Go over usage repos
        for repo in usage_repos:
            setattr(self, repo.name, self.is_used_in(repo))

    def __str__(self):
        return '{0: <100}'.format(self.name) + ' ' \
               + ' '.join([str(getattr(self, a))
                           for a in dir(self) if not a.startswith('__') and
                           not a == 'name' and not a.endswith('Lookup')
                           and not callable(getattr(self, a))])

    def has_jquery(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) for s in self.jqueryLookup])

    def is_react(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) for s in self.reactLookup])

    def is_es6(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) for s in self.es6Lookup])

    def is_in_component_factory(self, component_factory):
        return self.name.split('js/components/')[1].split('.')[0] in component_factory

    def is_used_in(self, repo):
        contents = repo.get_contents("")
        used_in = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif is_javascript(file_content.path):
                try:
                    decoded_content = file_content.decoded_content.decode("utf-8")
                    if self.check_usage(decoded_content):
                        used_in.append(file_content.path)
                except Exception as e:
                    print("Error " + str(e) + " " + self.name + '\n')
        return ' '.join(used_in)

    def check_usage(self, file_content):
        return self.name.split('.')[0] in file_content
