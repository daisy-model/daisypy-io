# pylint: disable=missing-module-docstring,missing-function-docstring
from daisypy.io.dai_util import parse_dai, format_dai

def test_leading_zeros_int():
    text = '''(defprogram LeadingZeros Daisy
    "Example" (time 1999 12 31) (stop 2001 01 01))'''
    expected = '''(defprogram LeadingZeros Daisy
  "Example" (time 1999 12 31) (stop 2001 1 1))'''
    for extended in False, True:
        parsed = parse_dai(text, extended=extended)
        assert format_dai(parsed) == expected

def test_leading_zeros_float():
    text = '''(defhorizon H H0\n  (clay 00.39 [%]))'''
    expected = '''(defhorizon H H0\n  (clay 0.39 [%]))'''
    for extended in False, True:
        parsed = parse_dai(text, extended=extended)
        assert format_dai(parsed) == expected

def test_parse_float():
    texts = [
        '(defhorizon H H0\n  (dry_bulk_density 12.3456 [g/cm^3]))',
        '(defhorizon H H0\n  (dry_bulk_density 12.34560 [g/cm^3]))',
        '(defhorizon H H0\n  (dry_bulk_density 012.3456 [g/cm^3]))',
        '(defhorizon H H0\n  (dry_bulk_density 0.123456e2 [g/cm^3]))',
    ]
    for text in texts:
        for extended in False, True:
            parsed = parse_dai(text, extended=extended)
            assert format_dai(parsed) == texts[0]

def test_parse_int():
    texts = [
        '(defhorizon H H0 (dry_bulk_density 1 [g/cm^3]))',
        '(defhorizon H H0 (dry_bulk_density 20 [g/cm^3]))',
        '(defhorizon H H0 (dry_bulk_density 0300 [g/cm^3]))',
        '(defhorizon H H0 (dry_bulk_density 1234567890 [g/cm^3]))',
    ]
    expected_values = [1, 20, 300, 1234567890]
    for text, expected in zip(texts, expected_values):
        for extended in False, True:
            parsed = parse_dai(text, extended=extended)
            assert parsed.values[0].body[0][1] == expected


def test_parse_mixed_number_list():
    text = '(defhorizon H H0 (list_of_numbers 0 0.0 -1 1.0 1234567890 -1234567890.0))'
    expected_values = [0, 0.0, -1, 1.0, 1234567890, -1234567890.0]
    expected_types = [int, float, int, float, int, float]
    for extended in False, True:
        parsed = parse_dai(text, extended=extended)
        values = parsed.values[0].body[0][1:]
        for n, expected_type, expected_val in zip(
                values, expected_types, expected_values, strict=True
        ):
            assert isinstance(n, expected_type)
            assert n == expected_val
