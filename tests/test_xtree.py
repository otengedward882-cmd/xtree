import unittest
import tempfile
import os
import shutil
import json
from pathlib import Path
from xtree import XTree, format_size


class TestXTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

        # Create sample structure
        (self.root / "src").mkdir()
        (self.root / "src" / "main.py").write_text("print('hello')")
        (self.root / "src" / "utils.py").write_text("# utils")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "index.md").write_text("# Docs")
        (self.root / ".hidden").write_text("secret")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_format_size(self):
        self.assertEqual(format_size(500).strip(), "500 B")
        self.assertEqual(format_size(1024).strip(), "1.0 KB")
        self.assertEqual(format_size(1024 * 1024).strip(), "1.0 MB")

    def test_render_basic(self):
        tree = XTree(root_dir=self.test_dir, no_color=True)
        output = tree.render()
        self.assertIn("src/", output)
        self.assertIn("main.py", output)
        self.assertIn("docs/", output)
        # Hidden files should be omitted by default
        self.assertNotIn(".hidden", output)

    def test_render_with_hidden(self):
        tree = XTree(root_dir=self.test_dir, show_hidden=True, no_color=True)
        output = tree.render()
        self.assertIn(".hidden", output)

    def test_dirs_only(self):
        tree = XTree(root_dir=self.test_dir, dirs_only=True, no_color=True)
        output = tree.render()
        self.assertIn("src/", output)
        self.assertNotIn("main.py", output)

    def test_max_depth(self):
        tree = XTree(root_dir=self.test_dir, max_depth=1, no_color=True)
        output = tree.render()
        self.assertIn("src/", output)
        self.assertNotIn("main.py", output)

    def test_json_export(self):
        tree = XTree(root_dir=self.test_dir)
        json_output = tree.to_json()
        data = json.loads(json_output)
        self.assertEqual(data["type"], "directory")
        self.assertTrue(any(c["name"] == "src" for c in data["children"]))

    def test_markdown_export(self):
        tree = XTree(root_dir=self.test_dir)
        md = tree.to_markdown()
        self.assertTrue(md.startswith("```text"))
        self.assertTrue(md.endswith("```"))


if __name__ == "__main__":
    unittest.main()
