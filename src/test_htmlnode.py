import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_children(self):
        child = HTMLNode("p", "Child node")
        parent = HTMLNode("div", "Parent", [child])
        self.assertEqual(parent.children, [child])

    def test_init_with_props(self):
        props = {"class": "main", "id": "test"}
        node = HTMLNode("div", "Content", props=props)
        self.assertEqual(node.props, props)

    def test_props_to_html_empty(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        props = {"class": "main", "id": "test"}
        node = HTMLNode("div", props=props)
        self.assertIn("class=main", node.props_to_html())
        self.assertIn("id=test", node.props_to_html())

    def test_to_html_not_implemented(self):
        node = HTMLNode("div", "Content")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("div", "Content", props={"class": "main"})
        repr_str = repr(node)
        self.assertIn("tag=div", repr_str)
        self.assertIn("value=Content", repr_str)
        self.assertIn("class", repr_str)

    def test_init_all_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


class TestLeafNode(unittest.TestCase):
    def test_leafnode_init(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_leafnode_with_props(self):
        props = {"class": "text-bold"}
        node = LeafNode("Hello", "span", props)
        self.assertEqual(node.props, props)

    def test_leafnode_to_html_with_tag(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode_to_html_no_tag(self):
        node = LeafNode("Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leafnode_to_html_with_props(self):
        node = LeafNode("Hello", "span")
        self.assertEqual(node.to_html(), "<span>Hello</span>")

    def test_leafnode_empty_value(self):
        node = LeafNode("")
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_parentnode_init(self):
        child = LeafNode("Hello", "p")
        node = ParentNode("div", [child])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [child])
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_parentnode_to_html_basic(self):
        child = LeafNode("Hello", "p")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_parentnode_to_html_with_props(self):
        child = LeafNode("Hello", "p")
        node = ParentNode("div", [child], {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class=container id=main><p>Hello</p></div>')

    def test_parentnode_to_html_nested(self):
        leaf1 = LeafNode("First", "p")
        leaf2 = LeafNode("Second", "p")
        inner = ParentNode("div", [leaf1, leaf2])
        outer = ParentNode("section", [inner])
        self.assertEqual(outer.to_html(), "<section><div><p>First</p><p>Second</p></div></section>")

    def test_parentnode_no_tag(self):
        child = LeafNode("Hello", "p")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parentnode_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )



if __name__ == "__main__":
    unittest.main()
