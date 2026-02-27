# pylint: disable=missing-module-docstring,missing-function-docstring
from daisypy.io.dai_util import format_dai
from daisypy.io.dai import Definition, Identifier, QuotedString, Comment, Dai, Input

def test_format_dai_def():
    single_threaded_spawn = Definition(
        Identifier('program'),
        Identifier('spawn1'),
        Identifier('spawn'),
        [ QuotedString('Single threaded spawn'), [Identifier('parallel'), 1] ]
    )
    formatted = format_dai(single_threaded_spawn)
    assert formatted == '(defprogram spawn1 spawn\n  "Single threaded spawn" (parallel 1))'

def test_format_comment():
    dai = Dai([
        Comment('Short comment'),
        Comment('Another short comment'),
        Comment('Line                                                                 wrapping '\
                'comment'),
    ])
    formatted = format_dai(dai, max_len=80)
    assert formatted == (
        ';; Short comment\n'\
        ';; Another short comment\n'\
        ';; Line                                                                 wrapping\n'\
        ';;  comment')

def test_format_short_comments():
    dai = Dai([
        Comment('a'),
        Comment('b'),
        Comment('c')
    ])
    formatted = format_dai(dai)
    assert formatted == ';; a\n;; b\n;; c'

def test_format_interleaved_comments():
    dai = Dai([
        Comment('c1'),
        Input('p1'),
        Comment('c2'),
        Input('p2'),
        Comment('c3'),
    ])
    formatted = format_dai(dai)
    assert formatted == ';; c1\n(input file p1)\n;; c2\n(input file p2)\n;; c3'
