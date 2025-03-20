import unittest
from text_type import TextType
from textnode import TextNode

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "This is a simple text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")

    def test_text_to_textnodes_italic(self):
        text = "This is *italic* text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://example.com) text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")

    def test_text_to_textnodes_image(self):
        text = "This is an ![image](https://example.com/img.png) text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.png")

    def test_text_to_textnodes_multiple(self):
        text = "This is **bold** and *italic* and `code` text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[5].text_type, TextType.CODE)

    def test_text_to_textnodes_complex(self):
        text = "This is a [link](https://example.com) and an ![image](https://example.com/img.png) with **bold** text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertTrue(any(node.text_type == TextType.LINK for node in nodes))
        self.assertTrue(any(node.text_type == TextType.IMAGE for node in nodes))
        self.assertTrue(any(node.text_type == TextType.BOLD for node in nodes))

    def test_text_to_textnodes_with_italic(self):
        text = "This is *italic* and _also italic_ text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "also italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text")

    def test_text_to_textnodes_with_italic_and_bold(self):
        text = "This is *italic* and **bold** and _also italic_ text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[4].text, " and ")
        self.assertEqual(nodes[5].text, "also italic")
        self.assertEqual(nodes[5].text_type, TextType.ITALIC)
        self.assertEqual(nodes[6].text, " text")

    def test_text_to_textnodes_with_nested_italic(self):
        text = "This is *italic with _nested_ italic* text"
        nodes = TextNode.text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "italic with _nested_ italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a different text node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.example.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_with_non_textnode(self):
        node = TextNode("Text", TextType.TEXT)
        self.assertNotEqual(node, "Not a TextNode")

    def test_str(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(str(node), "This is a text node")

    def test_repr(self):
        node = TextNode("Sample", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(Sample, bold, None)")

        node_with_url = TextNode("Link", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node_with_url), "TextNode(Link, link, https://example.com)")

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = TextNode.markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertTrue(all(isinstance(block, TextNode) for block in blocks))
        self.assertEqual(blocks[0].text.strip(), "This is **bolded** paragraph")
        self.assertEqual(blocks[1].text.strip(),
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line")
        self.assertEqual(blocks[2].text.strip(), "- This is a list\n- with items")
        self.assertTrue(all(block.text_type == TextType.TEXT for block in blocks))

    def test_markdown_to_blocks_empty_lines(self):
        md = """
        First paragraph


        Second paragraph

        Last paragraph"""
        blocks = TextNode.markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertTrue(all(isinstance(block, TextNode) for block in blocks))
        self.assertEqual(blocks[0].text.strip(), "First paragraph")
        self.assertEqual(blocks[1].text.strip(), "Second paragraph")
        self.assertEqual(blocks[2].text.strip(), "Last paragraph")
        self.assertTrue(all(block.text_type == TextType.TEXT for block in blocks))

    def test_markdown_to_blocks_whitespace_only(self):
        md = """
        First paragraph



        Last paragraph"""
        blocks = TextNode.markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertTrue(all(isinstance(block, TextNode) for block in blocks))
        self.assertEqual(blocks[0].text.strip(), "First paragraph")
        self.assertEqual(blocks[1].text.strip(), "Last paragraph")
        self.assertTrue(all(block.text_type == TextType.TEXT for block in blocks))

    def test_markdown_to_blocks_with_formatting(self):
        md = """
        **Bold** paragraph

        *Italic* paragraph

        `Code` block"""
        blocks = TextNode.markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertTrue(all(isinstance(block, TextNode) for block in blocks))
        self.assertEqual(blocks[0].text.strip(), "**Bold** paragraph")
        self.assertEqual(blocks[1].text.strip(), "*Italic* paragraph")
        self.assertEqual(blocks[2].text.strip(), "`Code` block")
        self.assertTrue(all(block.text_type == TextType.TEXT for block in blocks))

if __name__ == "__main__":
    unittest.main()