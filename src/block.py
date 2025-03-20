import re
from text_type import BlockType

def block_to_block_type(block: str) -> BlockType:
    """Determine the type of a markdown block.

    Args:
        block: A string containing a block of markdown text (stripped of leading/trailing whitespace)

    Returns:
        The BlockType of the block
    """
    # Check for empty block
    if not block:
        return BlockType.PARAGRAPH

    # Check for heading (1-6 # characters followed by space)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    # Check for code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE

    # Split into lines for multi-line block checks
    lines = block.split('\n')

    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Check for unordered list (every line starts with -)
    if all(line.strip().startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list (lines start with incrementing numbers)
    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH