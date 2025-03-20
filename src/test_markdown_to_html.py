import unittest
from markdown_to_html import (
    text_node_to_html_node,
    text_to_children,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    markdown_to_html_node,
)
from textnode import TextNode
from text_type import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertEqual(html.value, "Hello, world!")
        self.assertIsNone(html.tag)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.children[0].value, "Bold text")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.children[0].value, "Italic text")

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code text", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.children[0].value, "Code text")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.children[0].value, "Link text")
        self.assertEqual(html.props["href"], "https://example.com")

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.props["src"], "image.png")
        self.assertEqual(html.props["alt"], "Alt text")

    def test_text_to_children_simple(self):
        children = text_to_children("Hello, world!")
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].value, "Hello, world!")

    def test_text_to_children_complex(self):
        text = "Hello **bold** and *italic* and `code`"
        children = text_to_children(text)
        self.assertEqual(len(children), 6)
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[3].tag, "i")
        self.assertEqual(children[5].tag, "code")

    def test_paragraph_to_html_node(self):
        html = paragraph_to_html_node("Hello, world!")
        self.assertEqual(html.tag, "p")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].value, "Hello, world!")

    def test_heading_to_html_node(self):
        html = heading_to_html_node("# Heading 1")
        self.assertEqual(html.tag, "h1")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].value, "Heading 1")

        html = heading_to_html_node("### Heading 3")
        self.assertEqual(html.tag, "h3")

    def test_code_to_html_node(self):
        text = """```
print("Hello, world!")
```"""
        html = code_to_html_node(text)
        self.assertEqual(html.tag, "pre")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "code")
        self.assertEqual(html.children[0].children[0].value, 'print("Hello, world!")')

    def test_quote_to_html_node(self):
        text = "> This is a quote\n> Multiple lines"
        html = quote_to_html_node(text)
        self.assertEqual(html.tag, "blockquote")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].value, "This is a quote\nMultiple lines")

    def test_unordered_list_to_html_node(self):
        text = "- Item 1\n- Item 2\n- Item 3"
        html = unordered_list_to_html_node(text)
        self.assertEqual(html.tag, "ul")
        self.assertEqual(len(html.children), 3)
        self.assertTrue(all(child.tag == "li" for child in html.children))
        self.assertEqual(html.children[0].children[0].value, "Item 1")

    def test_ordered_list_to_html_node(self):
        text = "1. First\n2. Second\n3. Third"
        html = ordered_list_to_html_node(text)
        self.assertEqual(html.tag, "ol")
        self.assertEqual(len(html.children), 3)
        self.assertTrue(all(child.tag == "li" for child in html.children))
        self.assertEqual(html.children[0].children[0].value, "First")

    def test_markdown_to_html_node(self):
        markdown = """# Heading

This is a paragraph with **bold** and *italic* text.

```
def hello():
    print("Hello, world!")
```

> This is a quote

- List item 1
- List item 2

1. Ordered item 1
2. Ordered item 2"""

        html = markdown_to_html_node(markdown)
        self.assertEqual(html.tag, "div")
        self.assertTrue(len(html.children) > 0)

        # Check if each type of block is present
        tags = [child.tag for child in html.children]
        self.assertIn("h1", tags)
        self.assertIn("p", tags)
        self.assertIn("pre", tags)
        self.assertIn("blockquote", tags)
        self.assertIn("ul", tags)
        self.assertIn("ol", tags)

if __name__ == "__main__":
    unittest.main()