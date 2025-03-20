from __future__ import annotations

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        props_list = [f"{key}={value}" for key, value in self.props.items()]
        return " " + " ".join(props_list)

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    """A node that can't have children"""
    def __init__(self, value: str, tag: str = None, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        # Self-closing tags like img don't need a value
        if self.tag in ["img", "br", "hr"]:
            props = self.props_to_html()
            return f"<{self.tag}{props}>"

        if not self.value:
            raise ValueError("LeafNode must have a value")

        if not self.tag:
            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    """A node that can have children"""
    def __init__(self, tag: str, children: list = None, props: dict = None):
        super().__init__(tag, None, children or [], props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "".join(child.to_html() for child in self.children)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
