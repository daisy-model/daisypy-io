# pylint: disable=missing-module-docstring,missing-function-docstring
from daisypy.io.dai_util import parse_dai, format_dai

def test_leading_zeros_int():
    text = '''(defprogram LeadingZeros Daisy
    "Example" (time 1999 12 31) (stop 2001 01 01))'''
    expected = '''(defprogram LeadingZeros Daisy
  "Example" (time 1999 12 31) (stop 2001 1 1))'''
    parsed = parse_dai(text)
    assert format_dai(parsed) == expected

def test_leading_zeros_float():
    text = '''(defhorizon H (clay 00.39 [%]))'''
    expected = '''(defhorizon H (clay 0.39 [%]))'''
    parsed = parse_dai(text)
    assert format_dai(parsed) == expected
