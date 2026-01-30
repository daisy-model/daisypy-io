'''This is a very loose grammar that allows parsing dai files that are not actually valid.
Validation has to be performed after parsing'''

dai_grammar = '''
dai: top+

?top: sequence | comment
sequence: "(" sequence_val+ ")"
?sequence_val: value
             | sequence
             | comment

?value: integer | number | string 
?string: identifier | quoted_string | units

bool: /true|false/
integer.1: /0|[1-9][0-9]*/
number: SIGNED_NUMBER
identifier: /[a-zA-Z][a-zA-Z0-9=<>_+*\\/-]*/
quoted_string : ESCAPED_STRING
units: /\\[[^\\]]*\\]/ 
comment: /;.*/

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
'''
