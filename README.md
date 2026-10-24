 CSS Parser in Python

Project Overview
This project is a simple CSS parser developed using Python. It reads CSS input and converts CSS rules into structured JSON output.

Features
- Extracts CSS selectors and declarations.
- Supports multiple CSS rules and properties.
- Removes CSS comments while preserving comment-like text inside quoted strings.
- Handles semicolons and colons inside quoted values.
- Detects common syntax errors, such as missing braces, missing values, and unclosed comments or strings.
- Includes automated unit tests using Python's `unittest` framework.

Project Structure
```text
css-parser/
├── parser_writer.py
├── sample.css
├── README.md
└── tests/
    └── test_parser.py
```

Requirements
- Python 3

How to Run
Run the parser with a CSS file:

```bash
py parser_writer.py sample.css
```

The parser prints the parsed CSS rules as formatted JSON.

How to Run Tests
Run the following command from the project directory:

```bash
py -m unittest discover -s tests -v
```

 Current Test Status
All 13 unit tests pass.

Limitations
This is a basic CSS parser designed for simple CSS rules. It does not implement the complete CSS specification.
