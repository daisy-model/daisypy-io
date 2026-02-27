'''Formatting of Dai classes'''
import textwrap
from .dai_transformer import Definition, Path, Dai, Comment

def format_dai(dai, max_len=100, indent=0, top_level=True):
    '''Format Dai objects using a string representation that can be used as input file for Daisy.

    Parameters
    ----------
    dai: One of the Dai objects from daispy.io.dai

    max_len: int
      Maximum line length

    indent: int
      Indentation level

    top_level: bool
      If True indentation rules are adapted for top level

    Returns
    -------
    str
    '''
    indent_str = " " * indent

    if isinstance(dai, Dai):
        dai = dai.values

    if isinstance(dai, Path):
        dai = ['path'] + dai.values

    if isinstance(dai, Definition):
        def_part, body_part = dai.value
        def_part = format_dai(def_part, max_len-1, indent, top_level)
        body_part = format_dai(body_part, max_len, 0, False)[1:-1]
        # Instead of always adding a newline before body, we could try to fit verything on a single
        # line.
        # if len(def_part) + len(body_part) + 2 <= max_len:
        #     return "(" + def_part + " " + body_part + ")"
        indent_str = " " * (indent + 2)
        return "(" + def_part + "\n" + indent_str + body_part + ")"

    # Case 1: dai is not a list and can be converted directly to a string
    if not isinstance(dai, list):
        text = str(dai)
        if isinstance(dai, Comment):
            wrapped = textwrap.fill(
                text,
                width=max_len,
                replace_whitespace=False,
                drop_whitespace=False,
                initial_indent=indent_str,
                subsequent_indent=indent_str + ';; '
            )
        else:
            wrapped = textwrap.fill(
                text,
                width=max_len,
                initial_indent=indent_str,
                subsequent_indent=indent_str
            )
        return wrapped

    # Case 2: dai is a list
    items = [ format_dai(v, max_len, 0, False) for v in dai ]
    if top_level:
        # Everything on new line, no indentation
        return '\n'.join(items)

    nested_items = [ format_dai(v, max_len, indent+2, False) for v in dai ]
    comments = [ isinstance(v, Comment) for v in dai ]
    rows = []
    i = 0
    nested_indent = (indent + 2) * ' '
    for j, is_comment in enumerate(comments):
        if is_comment:
            # Try flat row
            row = " ".join(items[i:j])
            if len(row) <= max_len:
                rows.append(row)
            else:
                # Everything on new line
                rows += [items[i]] + [item for item in items[i+1:j]]
            rows.append(items[j])
            i = j+1
    if i < len(items):
        # Try flat row
        row = " ".join(items[i:])
        if len(row) <= max_len:
            rows.append(row)
        else:
            # Everything on new line
            rows += [items[i]] + [item for item in items[i+1:]]
    # Indent all rows except the first
    rows = [nested_indent + row if i > 0 else row for i, row in enumerate(rows)]
    return indent_str + "(" + "\n".join(rows) + ")"
