from pathlib import Path
from daisypy.io.dai_util import format_dai
from daisypy.io.dai import Definition, Identifier, QuotedString

def test_format_dai_def():
    single_threaded_spawn = Definition(
        Identifier('program'),
        Identifier('spawn1'),
        Identifier('spawn'),
        [ QuotedString('Single threaded spawn'), [Identifier('parallel'), 1] ]
    )
    formatted = format_dai(single_threaded_spawn)
    assert formatted == '(defprogram spawn1 spawn\n  "Single threaded spawn" (parallel 1))'
