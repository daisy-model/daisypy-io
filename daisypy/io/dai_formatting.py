'''Formatting of Dai classes'''
import textwrap
from .dai_transformer import Definition, Path, Dai, Comment

def format_dai(dai, max_len=100, indent=0, top_level=True):
    '''Format Dai objects using a string representation that can be used as input file for Daisy.

    dai: One of the Dai objects from daispy.io.dai

    max_len: int
      Maximum line length

    indent: int
      Indentation level

    top_level: bool
      If True indentation rules are adapted for top level

    Returns: str
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
        if isinstance(dai, Comment):
            # No wrapping when we have a comment
            return f'{indent_str}{dai}'
        dai = str(dai)
        return textwrap.fill(
            dai,
            width=max_len,
            initial_indent=indent_str,
            subsequent_indent=indent_str
        )

    # Case 2: dai is a list
    # TODO: Handle comments so we dont accidentally comments out the following line
    # Format children without indentation for flat-fit testing
    flat_items = [format_dai(v, max_len, 0, False).strip() for v in dai]

    # Build flat form: "(first rest rest)"
    if flat_items:
        flat = "(" + flat_items[0] + "".join(" " + x for x in flat_items[1:]) + ")"
    else:
        flat = "()"

    # If top-level, do NOT wrap in parentheses
    if top_level:
        # Try flat top-level (just join items)
        flat_top = " ".join(flat_items)
        if len(flat_top) <= max_len:
            return flat_top

        # Otherwise multiline top-level
        return "\n".join(format_dai(v, max_len, 0, False) for v in dai)

    # Non-top-level: try flat list
    if len(indent_str) + len(flat) <= max_len:
        return indent_str + flat

    # --- Multiline formatting ---
    # First element stays on same line as "(" with no space
    first = format_dai(dai[0], max_len, indent + 1, False).lstrip()
    lines = [f"{indent_str}({first}"]

    # Remaining elements each on their own line
    for item in dai[1:]:
        lines.append(format_dai(item, max_len, indent + 2, False))

    # Closing parenthesis attaches to last line
    lines[-1] = lines[-1] + ")"

    return "\n".join(lines).strip()
