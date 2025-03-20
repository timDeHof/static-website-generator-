import re
from text_type import TextType

class TextNode:
    __match_args__ = ("text", "text_type", "url")

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, TextNode)
            and self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def split_nodes_delimiter(old_nodes: list["TextNode"], delimiter: str, text_type: TextType) -> list["TextNode"]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue

            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Unclosed delimiter {delimiter} in text")

            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(parts[i], text_type))
        return new_nodes

    @staticmethod
    def split_nodes_image(old_nodes: list["TextNode"]) -> list["TextNode"]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            images = TextNode._extract_markdown_images(old_node.text)
            if not images:
                new_nodes.append(old_node)
                continue

            for alt_text, url in images:
                sections = original_text.split(f"![{alt_text}]({url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        return new_nodes

    @staticmethod
    def split_nodes_link(old_nodes: list["TextNode"]) -> list["TextNode"]:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            links = TextNode._extract_markdown_links(old_node.text)
            if not links:
                new_nodes.append(old_node)
                continue

            for link_text, url in links:
                sections = original_text.split(f"[{link_text}]({url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
        return new_nodes

    @staticmethod
    def _extract_markdown_images(text: str) -> list[tuple[str, str]]:
        return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    @staticmethod
    def _extract_markdown_links(text: str) -> list[tuple[str, str]]:
        return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    @staticmethod
    def text_to_textnodes(text: str) -> list["TextNode"]:
        """Convert a markdown text string into a list of TextNodes.

        Args:
            text: A string containing markdown text

        Returns:
            A list of TextNode objects representing the parsed markdown
        """
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = TextNode.split_nodes_image(nodes)  # Process images first
        nodes = TextNode.split_nodes_link(nodes)   # Then process links
        nodes = TextNode.split_nodes_delimiter(nodes, "**", TextType.BOLD)  # Process bold text
        nodes = TextNode.split_nodes_delimiter(nodes, "*", TextType.ITALIC)  # Process italic text with *
        nodes = TextNode.split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Process italic text with _
        nodes = TextNode.split_nodes_delimiter(nodes, "`", TextType.CODE)  # Process code blocks
        return nodes

    @staticmethod
    def markdown_to_blocks(markdown: str) -> list["TextNode"]:
        """Convert a markdown text string into a list of TextNode objects.

        Args:
            markdown: A string containing markdown text

        Returns:
            A list of TextNode objects representing the parsed markdown
        """
        # Split into blocks and normalize each block
        blocks = []
        for block in markdown.split("\n\n"):
            # Normalize whitespace in multi-line blocks
            lines = [line.strip() for line in block.strip().split("\n")]
            normalized_block = "\n".join(lines)
            if normalized_block:  # Skip empty blocks
                blocks.append(TextNode(normalized_block, TextType.TEXT))
        return blocks
