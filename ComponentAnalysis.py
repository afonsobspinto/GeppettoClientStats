from utils import last_modified_fix, is_phrase_in
import subprocess
import os


# Go over usage repos
# for r_name in USAGE_REPOS:
#     r = g.get_repo(r_name)
#     print(r.name)


class ComponentAnalysis:
    jqueryLookup = ['$', 'jQuery']
    reactLookup = ['react', 'componentWillMount', 'componentDidMount', 'shouldComponentUpdate', 'componentWillUpdate',
                   'componentDidUpdate', 'componentWillReceiveProps', 'shouldComponentUpdate',
                   'componentWillUpdate', 'componentDidUpdate', 'componentWillUnmount']
    es6Lookup = ['=>', 'let', 'const']

    def __init__(self, content, component_factory):
        self.name = content.path
        self.last_modified = last_modified_fix(content)
        decoded_content = content.decoded_content.decode("utf-8")

        # self.has_jquery = self.has_jquery(decoded_content)
        # self.is_react = self.is_react(decoded_content)
        # self.is_es6 = self.is_es6(decoded_content)
        self.is_in_component_factory = self.is_in_component_factory(component_factory)

    def __str__(self):
        return '{0: <100}'.format(self.name) + ' ' \
               + ' '.join([str(getattr(self, a))
                           for a in dir(self) if not a.startswith('__') and
                           not a == 'name' and not a.endswith('Lookup')
                           and not callable(getattr(self, a))])

    def has_jquery(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) in decoded_content for s in self.jqueryLookup])

    def is_react(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) for s in self.reactLookup])

    def is_es6(self, decoded_content):
        return any([is_phrase_in(s, decoded_content) for s in self.es6Lookup])

    def is_in_component_factory(self, component_factory):
        return self.name.split('js/components/')[1].split('.')[0] in component_factory
