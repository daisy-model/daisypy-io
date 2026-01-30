import textwrap

def format_dai(dai, max_len=80, indent=0, top_level=True):
    indent_str = " " * indent

    # Case 1: dai is not a list and can be converted directly to a string
    if not isinstance(dai, list):
        dai = str(dai)
        return textwrap.fill(
            dai,
            width=max_len,
            initial_indent=indent_str,
            subsequent_indent=indent_str
        )

    # Case 2: dai is a list 
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

    return "\n".join(lines)
