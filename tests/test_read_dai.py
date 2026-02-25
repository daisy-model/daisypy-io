from pathlib import Path
from daisypy.io.dai_util import read_dai, format_dai

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
        assert expected == formatted
    assert n_tests_run == 3
