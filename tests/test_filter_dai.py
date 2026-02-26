# pylint: disable=missing-module-docstring,missing-function-docstring
from daisypy.io.dai_util import format_dai, filter_dai
from daisypy.io.dai import Dai, Comment

def test_filter_dai():
    dai = Dai([
        Comment('1'), Comment('2'), Comment('3')
    ])

    dai = filter_dai(dai, lambda x: isinstance(x, Comment) and x.value != '3')
    print(dai)
    assert format_dai(dai) == ';; 1\n;; 2'
