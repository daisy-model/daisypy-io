# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path
import pytest
from daisypy.io.dai_util import read_dai, format_dai
from daisypy.io.exceptions import DaiException

def test_read_dai():
    in_dir = Path(__file__).parent / 'test-data' / 'valid-dai-files'
    n_tests_run = 0
    for in_path in in_dir.iterdir():
        if not in_path.suffix == '.dai':
            continue
        expected = in_path.read_text().rstrip('\n')
        dai = read_dai(in_path)
        formatted = format_dai(dai)
        n_tests_run += 1
        assert formatted == expected
    assert n_tests_run == 3

def test_read_extended():
    in_dir = Path(__file__).parent / 'test-data' / 'extended-grammar-files'
    n_tests_run = 0
    for in_path in in_dir.iterdir():
        if not in_path.suffix == '.dai':
            continue
        expected = in_path.read_text().rstrip('\n')
        with pytest.raises(DaiException):
            dai = read_dai(in_path, extended=False)
        dai = read_dai(in_path, extended=True)
        formatted = format_dai(dai)
        n_tests_run += 1
        assert formatted == expected
    assert n_tests_run == 1
