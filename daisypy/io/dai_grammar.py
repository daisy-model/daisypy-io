'''This is a very loose grammar that allows parsing dai files that are not actually valid.
Validation has to be performed after parsing'''

DAI_GRAMMAR = '''
dai: top+

?top: known_cmd | sequence | comment

?known_cmd : command | definition

?command : "(" top_level_cmd ")"
?top_level_cmd: input | run | directory | path | install_directory | allow_old_units | ui

input: "input" "file" quoted_string
run: "run" name
directory: "directory" quoted_string
path: "path" path_spec+
install_directory: "install_directory" quoted_string
allow_old_units: "allow_old_units" bool
ui: "ui" identifier

definition: "(" "def" identifier name name definition_body ")"
definition_body: sequence_val+

sequence: "(" sequence_val+ ")"
?sequence_val: value
             | sequence
             | comment

?value: integer | number | string
?string: identifier | quoted_string | units
?name: identifier | quoted_string
?path_spec: quoted_string | old
old: "&old"

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


DAI_GRAMMAR_EXTENDED = '''
dai: top+

?top: known_cmd | sequence | comment

?known_cmd : command | definition

?command : "(" top_level_cmd ")"
?top_level_cmd: input | run | directory | path | install_directory | allow_old_units | ui

input: "input" "file" quoted_string
run: "run" name
directory: "directory" quoted_string
path: "path" path_spec+
install_directory: "install_directory" quoted_string
allow_old_units: "allow_old_units" bool
ui: "ui" identifier

definition: "(" "def" identifier name name definition_body ")"
definition_body: sequence_val+

sequence: "(" sequence_val+ ")"
?sequence_val: value
             | sequence
             | comment

?value: integer | number | string | placeholder
?string: identifier | quoted_string | units
?name: identifier | quoted_string
?path_spec: quoted_string | old
placeholder: "{" placeholder_name "}"
?placeholder_name: /[a-zA-Z_][a-zA-Z0-9_]*/
old: "&old"

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
