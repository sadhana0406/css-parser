import json
import sys
from pathlib import Path



def remove_comments(css):
    """Remove CSS comments without changing quoted strings."""
    result = []
    i = 0
    quote = None
    escaped = False

    while i < len(css):
        char = css[i]

        # Preserve escaped characters and quoted strings.
        if escaped:
            result.append(char)
            escaped = False
            i += 1
            continue

        if char == "\\":
            result.append(char)
            escaped = True
            i += 1
            continue

        if quote:
            result.append(char)
            if char == quote:
                quote = None
            i += 1
            continue

        if char in ("'", '"'):
            quote = char
            result.append(char)
            i += 1
            continue

        # Remove comments only when outside quoted strings.
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)

            if end == -1:
                raise ValueError("Unclosed CSS comment")

            i = end + 2
            continue

        result.append(char)
        i += 1

    return "".join(result)



def parse_declarations(block):
    """Extract CSS property-value pairs safely."""
    declarations = {}

    # Split declarations only at semicolons outside strings.
    items = []
    start = 0
    quote = None
    escaped = False

    for i, char in enumerate(block):
        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == ";":
            items.append(block[start:i].strip())
            start = i + 1

    if quote is not None:
        raise ValueError("Unclosed string in declaration")

    items.append(block[start:].strip())

    for item in items:
        if not item:
            continue

        # Find the first colon outside strings.
        quote = None
        escaped = False
        colon = -1

        for i, char in enumerate(item):
            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if quote:
                if char == quote:
                    quote = None
            elif char in ("'", '"'):
                quote = char
            elif char == ":":
                colon = i
                break

        if quote is not None:
            raise ValueError("Unclosed string in declaration")

        if colon == -1:
            raise ValueError(f"Invalid declaration: {item}")

        name = item[:colon].strip()
        value = item[colon + 1:].strip()

        if not name or not value:
            raise ValueError(f"Invalid declaration: {item}")

        declarations[name] = value

    return declarations



def parse_css(css):
    """Convert simple CSS rules into structured data."""
    css = remove_comments(css)
    rules = []
    position = 0

    while position < len(css):
        position += len(css[position:]) - len(
            css[position:].lstrip()
        )

        if position >= len(css):
            break

        opening = css.find("{", position)

        if opening == -1:
            raise ValueError("Missing opening brace")

        selector = css[position:opening].strip()

        if not selector:
            raise ValueError("Missing selector")

        # Find the closing brace outside quoted strings.
        closing = -1
        quote = None
        escaped = False

        for i in range(opening + 1, len(css)):
            char = css[i]

            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if quote:
                if char == quote:
                    quote = None
            elif char in ("'", '"'):
                quote = char
            elif char == "}":
                closing = i
                break

        if quote is not None:
            raise ValueError("Unclosed string in CSS")

        if closing == -1:
            raise ValueError("Missing closing brace")

        block = css[opening + 1:closing]

        rules.append({
            "selector": selector,
            "declarations": parse_declarations(block)
        })

        position = closing + 1

    return {"rules": rules}


def main():
    if len(sys.argv) != 2:
        print("Usage: python parser_writer.py sample.css")
        sys.exit(1)

    try:
        css = Path(sys.argv[1]).read_text(encoding="utf-8")
        result = parse_css(css)
        print(json.dumps(result, indent=2))

    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
