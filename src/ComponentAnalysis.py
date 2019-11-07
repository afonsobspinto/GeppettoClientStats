from src.UsageAnalysis import UsageAnalysis
from src.utils import last_modified_fix, is_phrase_in


class ComponentAnalysis:
    jqueryLookup = ['$', 'jQuery']
    reactLookup = ['react', 'componentWillMount', 'componentDidMount', 'shouldComponentUpdate', 'componentWillUpdate',
                   'componentDidUpdate', 'componentWillReceiveProps', 'shouldComponentUpdate',
                   'componentWillUpdate', 'componentDidUpdate', 'componentWillUnmount']
    es6Lookup = ['=>', 'let', 'const']
    GEPPETTO = 'GEPPETTO\.'
    G = 'G\.'

    def __init__(self, content, component_factory, _type):
        self.name = content.path
        self.last_modified = last_modified_fix(content)
        self.type = _type
        decoded_content = content.decoded_content.decode("utf-8")
        self.has_jquery = self.has_jquery(decoded_content)
        self.is_react = self.is_react(decoded_content)
        self.is_es6 = self.is_es6(decoded_content)
        self.has_geppetto_global = self.has_geppetto_global(decoded_content)
        self.has_g_global = self.has_g_global(decoded_content)
        self.is_in_component_factory = self.is_in_component_factory(component_factory)
        self.usage_analysis = UsageAnalysis(self.name)

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

    def has_geppetto_global(self, decoded_content):
        return is_phrase_in(self.GEPPETTO, decoded_content)

    def has_g_global(self, decoded_content):
        return is_phrase_in(self.G, decoded_content)

    def check_usage(self, file_content, file_path, repo_name):
        self.usage_analysis.check_usage(file_content, file_path, repo_name)

    def get_row(self):
        r = [self.name, self.type, self.last_modified, self.usage_analysis.get_total_usage(), self.has_jquery,
             self.is_react, self.is_es6, self.has_geppetto_global, self.has_g_global, self.is_in_component_factory]
        for i in self.usage_analysis.get_row():
            r += [i]
        return r


