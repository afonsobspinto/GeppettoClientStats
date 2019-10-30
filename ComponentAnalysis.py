from settings import COLUMNS


class ComponentAnalysis:
    def __init__(self, name):
        self.name = name
        for entry in COLUMNS:
            setattr(self, entry, None)

    def __str__(self):
        return '{0: <100}'.format(self.name) + ' ' \
               + ' '.join([str(getattr(self, a))
                           for a in dir(self) if not a.startswith('__') and not a == 'name'
                           and not callable(getattr(self, a))])

