'''Transform dai parse tree
Comment, units, identifier and quoted strings are represented with classes.
These clases all have a __str__ that formats their value.
'''
from lark import Transformer

class DaiTransformer(Transformer):
    def comment(self, tokens):
        return Comment(tokens[0].value.lstrip('; '))

    def identifier(self, tokens):
        return Identifier(tokens[0].value)

    def quoted_string(self, tokens):
        return QuotedString(tokens[0].value[1:-1])

    def units(self, tokens):
        return Units(tokens[0].value[1:-1])

    def integer(self, tokens):
        return int(tokens[0].value)

    def number(self, tokens):
        return float(tokens[0].value)

    def bool(self, tokens):
        return tokens[0].value == 'true'

    def sequence(self, tokens):
        return tokens

    def dai(self, tokens):
        return tokens

class Comment:
    def __init__(self, value):
        self.value = value        
    def __repr__(self):
        return f'Comment({self.value})'
    def __str__(self):
        return f';; {self.value}'
        
class Identifier:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Identifier({self.value})'
    def __str__(self):
        return self.value

class QuotedString:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'QuotedString({self.value})'
    def __str__(self):
        return f'"{self.value}"'
    
class Units:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Units({self.value})'
    def __str__(self):
        return f'[{self.value}]'
