from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_type import TextType, BlockType
from block import block_to_block_type

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """Convert a TextNode to an HTMLNode."""
    if text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return ParentNode("b", [LeafNode(text_node.text)])
    elif text_node.text_type == TextType.ITALIC:
        return ParentNode("i", [LeafNode(text_node.text)])
    elif text_node.text_type == TextType.CODE:
        return ParentNode("code", [LeafNode(text_node.text)])
    elif text_node.text_type == TextType.LINK:
        return ParentNode("a", [LeafNode(text_node.text)], {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def text_to_children(text: str) -> list[HTMLNode]:
    """Convert markdown text to a list of HTMLNode children."""
    nodes = TextNode.text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT and not node.text.strip():
            continue  # Skip empty text nodes
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def paragraph_to_html_node(text: str) -> HTMLNode:
    """Convert a paragraph block to an HTMLNode."""
    return ParentNode("p", text_to_children(text))

def heading_to_html_node(text: str) -> HTMLNode:
    """Convert a heading block to an HTMLNode."""
    level = len(text.split()[0])  # Count the number of # characters
    return ParentNode(f"h{level}", text_to_children(text.lstrip("#").strip()))

def code_to_html_node(text: str) -> HTMLNode:
    """Convert a code block to an HTMLNode."""
    # Remove the ``` delimiters and get the content
    lines = text.split("\n")
    if len(lines) > 2:
        code_content = "\n".join(lines[1:-1])
    else:
        code_content = ""

    # Create a text node without parsing markdown
    code_node = ParentNode("code", [LeafNode(code_content)])
    return ParentNode("pre", [code_node])

def quote_to_html_node(text: str) -> HTMLNode:
    """Convert a quote block to an HTMLNode."""
    # Remove the > characters and convert the content
    lines = [line.lstrip(">").strip() for line in text.split("\n")]
    return ParentNode("blockquote", text_to_children("\n".join(lines)))

def unordered_list_to_html_node(text: str) -> HTMLNode:
    """Convert an unordered list block to an HTMLNode."""
    items = []
    for line in text.split("\n"):
        item_text = line.lstrip("- ").strip()
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)

def ordered_list_to_html_node(text: str) -> HTMLNode:
    """Convert an ordered list block to an HTMLNode."""
    items = []
    for line in text.split("\n"):
        item_text = line.split(". ", 1)[1].strip()
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)

def block_to_html_node(block: str) -> HTMLNode:
    """Convert a markdown block to an HTMLNode based on its type."""
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError(f"Invalid block type: {block_type}")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Convert a markdown document to an HTMLNode tree.

    Args:
        markdown: A string containing the markdown document

    Returns:
        An HTMLNode representing the root of the document
    """
    # Create parent div
    parent = ParentNode("div", [])

    # Split markdown into blocks and process each one
    blocks = TextNode.markdown_to_blocks(markdown)
    for block in blocks:
        parent.children.append(block_to_html_node(block.text))

    return parent