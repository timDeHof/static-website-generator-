import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_text_type_values(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "bold")
        self.assertEqual(TextType.ITALIC.value, "italic")
        self.assertEqual(TextType.CODE.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")

    def test_init_with_text_type(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_with_url(self):
        url = "https://example.com"
        node = TextNode("Link", TextType.LINK, url)
        self.assertEqual(node.text, "Link")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, url)

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

    def test_image_node(self):
        node = TextNode("alt text", TextType.IMAGE, "image.png")
        self.assertEqual(node.text, "alt text")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.url, "image.png")


if __name__ == "__main__":
    unittest.main()