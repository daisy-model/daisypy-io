# pylint: disable=missing-module-docstring,missing-function-docstring
from pathlib import Path

from daisypy.io.dlf import read_dlf


def test_read_dlf():
    in_path = (
        Path(__file__).parent
        / 'test-data'
        / 'valid-dlf-files'
        / 'blank_line_between_colnames_and_units.dlf'
    )
    dlf = read_dlf(in_path)

    assert dlf.header['dlf-version'] == '0.0'
    assert dlf.header['dlf-component'] == 'Sample water content'
    assert dlf.header['LOG'] == [
        'Average water content in two intervals.',
        'This could be used for comparison with, say, TDR probes.',
    ]
    assert dlf.units == {
        'year': '',
        'month': '',
        'mday': '',
        'hour': '',
        'Theta @ -15': '%',
        'Theta @ -30': '%',
        'Theta @ -45': '%',
        'Theta @ -60': '%',
    }
    assert dlf.body.to_dict(orient='records') == [{
        'year': 2026,
        'month': 1,
        'mday': 1,
        'hour': 1,
        'Theta @ -15': 23,
        'Theta @ -30': 32.3273,
        'Theta @ -45': 30.35,
        'Theta @ -60': 26.6,
    }]
