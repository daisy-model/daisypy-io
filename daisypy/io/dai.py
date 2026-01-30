from pathlib import Path
from lark import Lark
from .dai_grammar import dai_grammar
from .dai_transformer import DaiTransformer
from .dai_formatting import format_dai
from .exceptions import DaiException

__all__ = [
    'parse_dai',
    'transform_dai',
    'format_dai',
    'read_dai',
    'write_dai',
    'DaiException'
]

dai_parser = Lark(dai_grammar, start="dai")
dai_transformer = DaiTransformer()

def parse_dai(text):
    return dai_parser.parse(text)

def transform_dai(parse_tree):
    return dai_transformer.transform(parse_tree)

def read_dai(path):
    path = Path(path)
    text = path.read_text()
    try:
        parsed = parse_dai(text)
        return transform_dai(parsed)
    except UnexpectedInput:
        raise DaiException("Parse error")
    except VisitError:
        raise DaiException("Transformation error")

def write_dai(dai, out_path):
    out_path = Path(out_path)
    out_path.write_text(format_dai(dai))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inpath')
    args = parser.parse_args()
    dai = read_dai(args.inpath)
    formatted = format_dai(dai)
    print(formatted)
