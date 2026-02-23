'''Data types for dai files'''

class Dai:
    def __init__(self, values):
        self.values = values
    def __repr__(self):
        return f'Dai({", ".join(repr(v) for v in self.values)})'
    def __str__(self):
        return '\n'.join((str(v) for v in self.values))

class Comment:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Comment({repr(self.value)})'
    def __str__(self):
        return f';; {self.value}'

class Identifier:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Identifier({repr(self.value)})'
    def __str__(self):
        return self.value

class QuotedString:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'QuotedString({repr(self.value)})'
    def __str__(self):
        return f'"{self.value}"'

class Units:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Units({repr(self.value)})'
    def __str__(self):
        return f'[{self.value}]'

class Input:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Input({repr(self.value)})'
    def __str__(self):
        return f'(input file {self.value})'

class Definition:
    def __init__(self, component, name, parent, body):
        self.component = component
        self.name = name
        self.parent = parent
        self.body = body
    @property
    def value(self):
        return [f'def{self.component} {self.name} {self.parent}', self.body]
    def __repr__(self):
        return f'Definition({repr(self.component)}, {repr(self.name)}, {repr(self.parent)}, {repr(self.body)})'

class Run:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Run({repr(self.value)})'
    def __str__(self):
        return f'(run {self.value})'

class Ui:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Ui({repr(self.value)})'
    def __str__(self):
        return f'(ui {self.value})'

class Directory:
    def __init__(self, value):
        if not isinstance(value, QuotedString):
            self.value = QuotedString(str(value))
        else:
            self.value = value
    def __repr__(self):
        return f'Directory({repr(self.value)})'
    def __str__(self):
        return f'(directory {self.value})'

class Path:
    def __init__(self, values):
        self.values = [
            v if isinstance(v, QuotedString) or isinstance(v, Old)
            else QuotedString(str(v)) for v in values
        ]
    def __repr__(self):
        return f'Path({", ".join((repr(v) for v in self.values))})'
    def __str__(self):
        return f'(path {", ".join((str(v) for v in self.values))})'

class Old:
    def __repr__(self):
        return 'Old()'
    def __str__(self):
        return '&old'


def get_run(dai):
    for cmd in dai:
        if isinstance(cmd, Run):
            return cmd
    return None
