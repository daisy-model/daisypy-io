'''Transform dai parse tree
Comment, units, identifier and quoted strings are represented with classes.
These clases all have a __str__ that formats their value.
'''
from lark import Transformer
from .dai import (
    Dai, Run, Ui, Path, Old, Directory, Definition, Input, Units, QuotedString, Identifier, Comment,
    Placeholder
)

class DaiTransformer(Transformer):
    # pylint: disable=missing-function-docstring, missing-class-docstring
    def definition(self, tokens):
        return Definition(*tokens)

    def definition_body(self, tokens):
        return tokens

    def input(self, tokens):
        return Input(tokens[0])

    def run(self, tokens):
        return Run(tokens[0])

    def ui(self, tokens):
        return Ui(tokens[0])

    def old(self, _tokens):
        return Old()

    def directory(self, tokens):
        return Directory(tokens[0])

    def path(self, tokens):
        return Path(tokens)

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

    def placeholder(self, tokens):
        return Placeholder(tokens[0])

    def sequence(self, tokens):
        return tokens

    def dai(self, tokens):
        return Dai(tokens)
