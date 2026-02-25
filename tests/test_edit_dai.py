from pathlib import Path
from daisypy.io.dai_util import read_dai, format_dai
from daisypy.io.dai import Definition, Identifier, QuotedString, Comment

def test_format_dai_def():
    expected_path = Path(__file__).parent / 'test-data' / 'valid-dai-files' / 'test-spawn1.dai'
    expected = format_dai(read_dai(expected_path))

    in_path = Path(__file__).parent / 'test-data' / 'valid-dai-files' / 'test-spawn.dai'
    dai = read_dai(in_path)

    assert format_dai(dai) != expected

    # Replace all references to spawn with a reference to spawn1
    for value in dai.values:
        if isinstance(value, Definition) and value.parent.value == 'spawn':
            value.parent.value = 'spawn1'

    # Add definition of spawn1 to top of file
    single_threaded_spawn = Definition(
        Identifier('program'),
        Identifier('spawn1'),
        Identifier('spawn'),
        [ QuotedString('Single threaded spawn'), [Identifier('parallel'), 1] ]
    )
    for i, value in enumerate(dai.values):
        if not isinstance(value, Comment):
            dai.values.insert(i, single_threaded_spawn)
            break

    assert format_dai(dai) == expected
