'''Utilities for working with dai files and Dai objects'''
from pathlib import Path
from lark import Lark
from lark.exceptions import UnexpectedInput, VisitError
from .dai_transformer import DaiTransformer
from .dai_formatting import format_dai
from .dai_grammar import DAI_GRAMMAR
from .exceptions import DaiException

dai_parser = Lark(DAI_GRAMMAR, start="dai")

def parse_dai(text):
    '''Parse a Dai object from text

    Returns
    -------
    A Dai object'''
    try:
        return dai_parser.parse(text)
    except UnexpectedInput as e:
        raise DaiException("Parse error") from e


dai_transformer = DaiTransformer()

def transform_dai(parse_tree):
    '''Transform a Dai object to a string

    Returns
    -------
    str
    '''
    try:
        return dai_transformer.transform(parse_tree)
    except VisitError as e:
        raise DaiException("Transformation error") from e

def read_dai(path):
    '''Read a .dai file

    Returns
    -------
    A Dai object
    '''
    path = Path(path)
    text = path.read_text(encoding='utf-8')
    parsed = parse_dai(text)
    return transform_dai(parsed)

def write_dai(dai, out_path):
    '''Write a Dai object to a .dai file that can be read by Daisy'''
    out_path = Path(out_path)
    out_path.write_text(format_dai(dai), encoding='utf-8')

def main(inpath):
    dai = read_dai(inpath)
    formatted = format_dai(dai)
    print(formatted)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inpath')
    args = parser.parse_args()
    main(args.inpath)
