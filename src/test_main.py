import unittest
import os
import tempfile
import shutil
from main import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#  Hello  "
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_content_after(self):
        markdown = "# Hello\n\nThis is a paragraph"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_content_before(self):
        markdown = "Some text\n\n# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_other_headings(self):
        markdown = "# Main Title\n\n## Subtitle\n\n### Smaller Title"
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_extract_title_no_heading(self):
        markdown = "This is just a paragraph"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_h2_only(self):
        markdown = "## This is not an h1"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_h1s(self):
        markdown = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_extract_title_with_formatting(self):
        markdown = "# **Bold** and *italic* title"
        self.assertEqual(extract_title(markdown), "**Bold** and *italic* title")

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()

        # Create test markdown file
        self.markdown_path = os.path.join(self.temp_dir, "test.md")
        with open(self.markdown_path, "w") as f:
            f.write("# Test Title\n\nThis is a test paragraph.")

        # Create test template file
        self.template_path = os.path.join(self.temp_dir, "template.html")
        with open(self.template_path, "w") as f:
            f.write("<!DOCTYPE html><html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        # Set destination path
        self.dest_path = os.path.join(self.temp_dir, "output.html")

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_generate_page(self):
        # Generate the page
        generate_page(self.markdown_path, self.template_path, self.dest_path)

        # Check if file was created
        self.assertTrue(os.path.exists(self.dest_path))

        # Read the generated HTML
        with open(self.dest_path, "r") as f:
            html = f.read()

        # Check if title and content were properly inserted
        self.assertIn("Test Title", html)
        self.assertIn("This is a test paragraph", html)

    def test_generate_page_nested_directories(self):
        # Create a nested destination path
        nested_dest = os.path.join(self.temp_dir, "nested", "output.html")

        # Generate the page
        generate_page(self.markdown_path, self.template_path, nested_dest)

        # Check if file was created in nested directory
        self.assertTrue(os.path.exists(nested_dest))

    def test_generate_page_invalid_markdown(self):
        # Create invalid markdown (no h1)
        with open(self.markdown_path, "w") as f:
            f.write("This is invalid markdown without a title")

        # Should raise ValueError when trying to extract title
        with self.assertRaises(ValueError):
            generate_page(self.markdown_path, self.template_path, self.dest_path)

    def test_generate_page_invalid_template(self):
        # Create invalid template (missing placeholders)
        with open(self.template_path, "w") as f:
            f.write("<!DOCTYPE html><html><body>No placeholders</body></html>")

        # Generate the page (should still work, just without replacements)
        generate_page(self.markdown_path, self.template_path, self.dest_path)

        # Check if file was created
        self.assertTrue(os.path.exists(self.dest_path))

if __name__ == "__main__":
    unittest.main()