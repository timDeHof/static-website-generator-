import unittest
from text_type import BlockType
from block import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Empty block should be paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

        # Multi-line paragraph
        block = "This is a paragraph\nwith multiple\nlines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Invalid headings should be paragraphs
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code(self):
        # Simple code block
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Code block with language
        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Invalid code blocks should be paragraphs
        self.assertEqual(block_to_block_type("```\nUnclosed code"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("`Not a code block`"), BlockType.PARAGRAPH)

    def test_quote(self):
        # Single line quote
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)

        # Multi-line quote
        block = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Invalid quotes should be paragraphs
        self.assertEqual(block_to_block_type(">First line\nSecond line"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)

        # Multiple items
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Invalid lists should be paragraphs
        self.assertEqual(block_to_block_type("- First item\nNot an item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)

        # Multiple items
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Invalid lists should be paragraphs
        self.assertEqual(block_to_block_type("1. First\nNot numbered"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. First\n3. Wrong number"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()