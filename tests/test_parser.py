import unittest

from parser_writer import parse_css


class TestCSSParser(unittest.TestCase):

    def test_basic_rule(self):
        result = parse_css(".title { color: blue; }")
        self.assertEqual(
            result["rules"][0]["selector"], ".title"
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["color"],
            "blue"
        )
    def test_unclosed_string(self):
        with self.assertRaises(ValueError):
            parse_css('.box { content: "hello; }')   

    def test_multiple_properties(self):
        result = parse_css(
            ".box { color: red; padding: 10px; }"
        )
        declarations = result["rules"][0]["declarations"]
        self.assertEqual(len(declarations), 2)

    def test_comments(self):
        result = parse_css(
            "/* comment */ .box { color: red; }"
        )
        self.assertEqual(len(result["rules"]), 1)

    def test_empty_css(self):
        result = parse_css("")
        self.assertEqual(result["rules"], [])

    def test_missing_closing_brace(self):
        with self.assertRaises(ValueError):
            parse_css(".box { color: red;")

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            parse_css(".box { color: ; }")

    def test_unclosed_comment(self):
        with self.assertRaises(ValueError):
            parse_css("/* unfinished comment")

    def test_duplicate_property(self):
        result = parse_css(
            ".box { color: red; color: blue; }"
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["color"],
            "blue"
        )
        
    def test_multiple_selectors(self):
        result = parse_css("h1, h2 { color: green; }")
        self.assertEqual(
            result["rules"][0]["selector"], "h1, h2"
        )

    def test_colon_in_value(self):
        result = parse_css(
            ".box { background: url(http://example.com/a); }"
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["background"],
            "url(http://example.com/a)"
        )
    def test_semicolon_inside_string(self):
        result = parse_css(
            '.box { content: "hello; world"; }'
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["content"],
            '"hello; world"'
        )
    def test_semicolon_inside_string(self):
        result = parse_css(
            '.box { content: "hello; world"; }'
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["content"],
            '"hello; world"'
        )
        
    def test_comment_marker_inside_string(self):
        result = parse_css(
            '.box { content: "/* not a comment */"; }'
        )
        self.assertEqual(
            result["rules"][0]["declarations"]["content"],
            '"/* not a comment */"'
        )

        



        

    


if __name__ == "__main__":
    unittest.main()
