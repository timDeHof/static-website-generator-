import os
import sys
import shutil
import logging
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from markdown_to_html import markdown_to_html_node

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str = "/") -> None:
    """
    Generate an HTML page from a markdown file using a template.

    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template
        dest_path: Path where the generated HTML should be saved
        base_path: Base path for the site (defaults to "/")
    """
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, "r") as f:
        markdown = f.read()

    # Read template file
    with open(template_path, "r") as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders in template
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)

    # Ensure base_path ends with a slash for proper URL joining
    if not base_path.endswith("/"):
        base_path = base_path + "/"

    # Replace href="/ and src="/ with the base path
    # Handle both quoted and unquoted attributes
    html_page = html_page.replace('href="/', f'href="{base_path}')
    html_page = html_page.replace('src="/', f'src="{base_path}')
    html_page = html_page.replace("href='/", f"href='{base_path}")
    html_page = html_page.replace("src='/", f"src='{base_path}")
    # Handle attributes without quotes
    html_page = html_page.replace('href=/', f'href={base_path}')
    html_page = html_page.replace('src=/', f'src={base_path}')

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML to file
    with open(dest_path, "w") as f:
        f.write(html_page)

    logging.info(f"Generated {dest_path}")

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str = "/") -> None:
    """
    Recursively generate HTML pages from markdown files in a directory using a template.

    Args:
        dir_path_content: Path to the directory containing markdown files
        template_path: Path to the HTML template
        dest_dir_path: Path where the generated HTML files should be saved
        base_path: Base path for the site (defaults to "/")
    """
    logging.info(f"Generating pages recursively from {dir_path_content} to {dest_dir_path} using {template_path}")

    # Ensure destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    # Iterate over files in the directory
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        # If it's a file, generate the page
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, base_path)
        # If it's a directory, recurse
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, base_path)

def copy_static_to_public(source_dir: str, dest_dir: str) -> None:
    """
    Recursively copy all contents from source_dir to dest_dir.
    First deletes all contents of dest_dir to ensure a clean copy.

    Args:
        source_dir: Source directory path
        dest_dir: Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        logging.info(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create destination directory
    os.makedirs(dest_dir)

    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        # Get the relative path from source_dir
        rel_path = os.path.relpath(root, source_dir)
        # Create corresponding directory in destination
        dest_path = os.path.join(dest_dir, rel_path)

        # Create directories
        for dir_name in dirs:
            full_dir_path = os.path.join(dest_path, dir_name)
            os.makedirs(full_dir_path)
            logging.info(f"Created directory: {full_dir_path}")

        # Copy files
        for file_name in files:
            source_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_path, file_name)
            shutil.copy2(source_file, dest_file)
            logging.info(f"Copied file: {dest_file}")

def extract_title(markdown: str) -> str:
    """
    Extract the h1 heading from markdown text.

    Args:
        markdown: A string containing markdown text

    Returns:
        The text of the h1 heading (without the # and whitespace)

    Raises:
        ValueError: If no h1 heading is found
    """
    # Split markdown into blocks
    blocks = TextNode.markdown_to_blocks(markdown)

    # Look for a block that starts with a single #
    for block in blocks:
        text = block.text.strip()
        if text.startswith("# "):
            return text[2:].strip()

    raise ValueError("No h1 heading found in markdown")

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.LINK:
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(text_node.text, "b")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(text_node.text, "i")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(text_node.text, "code")
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(text_node.text, "img", {"src": text_node.url})
    else:
        raise ValueError("Invalid text node")

def main(*argv):
    # Get base path from command line arguments or use default
    base_path = argv[0] if argv else "/"

    # Ensure base path starts with /
    if not base_path.startswith("/"):
        base_path = "/" + base_path

    # Copy static files to public directory
    copy_static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)

if __name__ == "__main__":
    main(*sys.argv[1:])
