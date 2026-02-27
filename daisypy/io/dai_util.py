'''Utilities for working with dai files and Dai objects'''
import pathlib
from lark import Lark
from lark.exceptions import UnexpectedInput, VisitError
from .dai import Dai, Definition, Path
from .dai_transformer import DaiTransformer
from .dai_formatting import format_dai
from .dai_grammar import DAI_GRAMMAR, DAI_GRAMMAR_EXTENDED
from .exceptions import DaiException

dai_parser = Lark(DAI_GRAMMAR, start="dai")
dai_parser_extended = Lark(DAI_GRAMMAR_EXTENDED, start="dai")
dai_transformer = DaiTransformer()

def parse_dai(text, extended=False):
    '''Parse a Dai object from text

    Parameters
    ----------
    text : str

    extended : bool
      If True use extended grammar that included placeholders "{ placeholder_name }"

    Returns
    -------
    Dai object
    '''
    try:
        if not extended:
            parse_tree = dai_parser.parse(text)
        else:
            parse_tree = dai_parser_extended.parse(text)
        return dai_transformer.transform(parse_tree)
    except UnexpectedInput as e:
        raise DaiException("Parse error") from e
    except VisitError as e:
        raise DaiException("Transformation error") from e

def read_dai(path, extended=False):
    '''Read a .dai file

    Returns
    -------
    A Dai object
    '''
    path = pathlib.Path(path)
    text = path.read_text(encoding='utf-8')
    return parse_dai(text, extended)

def write_dai(dai, out_path):
    '''Write a Dai object to a .dai file that can be read by Daisy'''
    out_path = pathlib.Path(out_path)
    out_path.write_text(format_dai(dai), encoding='utf-8')

def filter_dai(dai, predicate):
    '''Drop all parts of Dai object that do not satisfy a predicate'''
    assert isinstance(dai, Dai)
    return Dai([_filter_dai(value, predicate) for value in dai.values if predicate(value)])

def _filter_dai(dai, predicate):
    # We need to handle definition and path because they have nested components
    # the rest are just returned as is
    if isinstance(dai, Definition):
        return Definition(
            dai.component,
            dai.name,
            dai.parent,
            [_filter_dai(value, predicate) for value in dai.body if predicate(value)]
        )
    if isinstance(dai, Path):
        return Path([value for value in dai.values if predicate(value)])
    return dai
