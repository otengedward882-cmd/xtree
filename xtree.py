#!/usr/bin/env python3
"""
xtree - eXtended Tree CLI
==========================
A lightweight, modern directory tree visualizer and project inspector.
Zero external dependencies. Pure Python 3 standard library.

Author: otengedward882-cmd
License: MIT
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

__version__ = "1.0.0"

# ANSI Colors for terminal output
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


DEFAULT_IGNORES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
    "dist",
    "build",
    "*.pyc",
}

EXT_COLORS = {
    # Code
    ".py": Colors.GREEN,
    ".js": Colors.YELLOW,
    ".ts": Colors.CYAN,
    ".jsx": Colors.YELLOW,
    ".tsx": Colors.CYAN,
    ".html": Colors.MAGENTA,
    ".css": Colors.MAGENTA,
    ".json": Colors.YELLOW,
    ".c": Colors.CYAN,
    ".cpp": Colors.CYAN,
    ".h": Colors.CYAN,
    ".rs": Colors.YELLOW,
    ".go": Colors.CYAN,
    ".java": Colors.YELLOW,
    # Data & Docs
    ".md": Colors.BLUE,
    ".txt": Colors.DIM,
    ".csv": Colors.GREEN,
    ".yml": Colors.YELLOW,
    ".yaml": Colors.YELLOW,
    ".xml": Colors.MAGENTA,
    # Images & Media
    ".png": Colors.MAGENTA,
    ".jpg": Colors.MAGENTA,
    ".jpeg": Colors.MAGENTA,
    ".svg": Colors.MAGENTA,
    ".gif": Colors.MAGENTA,
    # Archives
    ".zip": Colors.BOLD,
    ".tar": Colors.BOLD,
    ".gz": Colors.BOLD,
}


def format_size(bytes_size: int) -> str:
    """Format bytes into human-readable size."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0 or unit == "TB":
            if unit == "B":
                return f"{bytes_size:4d} B"
            return f"{bytes_size:5.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:5.1f} PB"


class XTree:
    def __init__(
        self,
        root_dir: str = ".",
        max_depth: Optional[int] = None,
        show_sizes: bool = False,
        show_hidden: bool = False,
        dirs_only: bool = False,
        ignore_patterns: Optional[Set[str]] = None,
        pattern: Optional[str] = None,
        use_ascii: bool = False,
        no_color: bool = False,
    ):
        self.root = Path(root_dir).resolve()
        self.max_depth = max_depth
        self.show_sizes = show_sizes
        self.show_hidden = show_hidden
        self.dirs_only = dirs_only
        self.ignore_patterns = DEFAULT_IGNORES.union(ignore_patterns or set())
        self.pattern = pattern
        self.use_ascii = use_ascii
        self.no_color = no_color or not sys.stdout.isatty()

        # Metrics
        self.total_dirs = 0
        self.total_files = 0
        self.total_bytes = 0

        # Branch glyphs
        if self.use_ascii:
            self.branch = "|-- "
            self.last_branch = "`-- "
            self.pipe = "|   "
            self.space = "    "
        else:
            self.branch = "├── "
            self.last_branch = "└── "
            self.pipe = "│   "
            self.space = "    "

    def _should_ignore(self, path: Path) -> bool:
        """Determine if a path matches ignore criteria."""
        name = path.name
        if not self.show_hidden and name.startswith(".") and name != ".":
            return True
        if name in self.ignore_patterns:
            return True
        for pattern in self.ignore_patterns:
            if pattern.startswith("*") and name.endswith(pattern[1:]):
                return True
        return False

    def _matches_pattern(self, path: Path) -> bool:
        """Check if path matches user search pattern."""
        if not self.pattern:
            return True
        return path.match(self.pattern)

    def _color(self, text: str, color_code: str) -> str:
        """Apply ANSI color if enabled."""
        if self.no_color:
            return text
        return f"{color_code}{text}{Colors.RESET}"

    def build_tree_structure(self, current_dir: Path, current_depth: int = 0) -> List[Tuple[str, Path, bool]]:
        """Traverse and generate tree lines recursively."""
        if self.max_depth is not None and current_depth >= self.max_depth:
            return []

        try:
            entries = sorted(list(current_dir.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return [(" [Permission Denied]", current_dir, True)]

        # Filter entries
        valid_entries = [e for e in entries if not self._should_ignore(e)]
        if self.dirs_only:
            valid_entries = [e for e in valid_entries if e.is_dir()]

        results = []
        count = len(valid_entries)

        for index, entry in enumerate(valid_entries):
            is_last = (index == count - 1)
            results.append((entry, is_last, current_depth))

        return results

    def render(self) -> str:
        """Render the complete directory tree to string."""
        lines = []
        root_name = self.root.name or str(self.root)
        lines.append(self._color(f"{root_name}/", Colors.BOLD + Colors.BLUE))

        self._render_recursive(self.root, prefix="", current_depth=0, lines=lines)

        # Append summary statistics
        size_str = format_size(self.total_bytes) if self.show_sizes else ""
        size_part = f", Total Size: {size_str}" if self.show_sizes else ""
        summary = (
            f"\n📊 Summary: {self.total_dirs} directories, {self.total_files} files{size_part}"
        )
        lines.append(self._color(summary, Colors.DIM))

        return "\n".join(lines)

    def _render_recursive(self, current_dir: Path, prefix: str, current_depth: int, lines: List[str]):
        if self.max_depth is not None and current_depth >= self.max_depth:
            return

        try:
            entries = sorted(list(current_dir.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            lines.append(f"{prefix}└── [Permission Denied]")
            return

        valid_entries = [e for e in entries if not self._should_ignore(e)]
        if self.dirs_only:
            valid_entries = [e for e in valid_entries if e.is_dir()]

        count = len(valid_entries)

        for index, entry in enumerate(valid_entries):
            is_last = (index == count - 1)
            connector = self.last_branch if is_last else self.branch

            is_dir = entry.is_dir()
            size_tag = ""

            try:
                if is_dir:
                    self.total_dirs += 1
                    display_name = self._color(f"{entry.name}/", Colors.BOLD + Colors.BLUE)
                else:
                    self.total_files += 1
                    stat = entry.stat()
                    self.total_bytes += stat.st_size

                    if not self._matches_pattern(entry):
                        continue

                    ext = entry.suffix.lower()
                    color = EXT_COLORS.get(ext, Colors.RESET)
                    display_name = self._color(entry.name, color)

                    if self.show_sizes:
                        size_tag = f" {self._color(f'[{format_size(stat.st_size)}]', Colors.DIM)}"

            except OSError:
                display_name = f"{entry.name} [Error]"

            lines.append(f"{prefix}{connector}{display_name}{size_tag}")

            if is_dir:
                next_prefix = prefix + (self.space if is_last else self.pipe)
                self._render_recursive(entry, next_prefix, current_depth + 1, lines)

    def to_json(self) -> str:
        """Export tree as nested JSON dictionary."""
        def _build_dict(path: Path, depth: int = 0) -> Dict:
            item = {"name": path.name, "type": "directory" if path.is_dir() else "file"}
            if path.is_file():
                try:
                    item["size"] = path.stat().st_size
                except OSError:
                    item["size"] = 0
            elif path.is_dir() and (self.max_depth is None or depth < self.max_depth):
                children = []
                try:
                    for entry in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                        if not self._should_ignore(entry):
                            if not self.dirs_only or entry.is_dir():
                                children.append(_build_dict(entry, depth + 1))
                except PermissionError:
                    pass
                item["children"] = children
            return item

        data = _build_dict(self.root)
        return json.dumps(data, indent=2)

    def to_markdown(self) -> str:
        """Export tree wrapped in a clean Markdown code block."""
        tree_text = self.render()
        # Strip ANSI colors for markdown
        for code in [Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.CYAN, Colors.MAGENTA, Colors.BOLD, Colors.DIM, Colors.RESET]:
            tree_text = tree_text.replace(code, "")
        return f"```text\n{tree_text}\n```"


def main():
    parser = argparse.ArgumentParser(
        prog="xtree",
        description="🌿 xtree - eXtended directory tree visualizer and project inspector.",
        epilog="Examples:\n  xtree -s -L 2\n  xtree --markdown > structure.md\n  xtree -p '*.py'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("path", nargs="?", default=".", help="Target directory (default: current directory)")
    parser.add_argument("-L", "--depth", type=int, default=None, help="Max display depth of the directory tree")
    parser.add_argument("-s", "--sizes", action="store_true", help="Display human-readable file sizes")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files (starting with .)")
    parser.add_argument("-d", "--dirs-only", action="store_true", help="List directories only")
    parser.add_argument("-p", "--pattern", type=str, default=None, help="Filter files by glob pattern (e.g., '*.py')")
    parser.add_argument("-i", "--ignore", nargs="*", default=[], help="Additional directory or file names to ignore")
    parser.add_argument("--ascii", action="store_true", help="Use standard ASCII characters instead of Unicode")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--markdown", action="store_true", help="Output tree formatted inside a Markdown code block")
    parser.add_argument("--json", action="store_true", help="Output directory hierarchy as structured JSON")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    tree = XTree(
        root_dir=args.path,
        max_depth=args.depth,
        show_sizes=args.sizes,
        show_hidden=args.all,
        dirs_only=args.dirs_only,
        ignore_patterns=set(args.ignore),
        pattern=args.pattern,
        use_ascii=args.ascii,
        no_color=args.no_color,
    )

    if args.json:
        print(tree.to_json())
    elif args.markdown:
        print(tree.to_markdown())
    else:
        print(tree.render())


if __name__ == "__main__":
    main()
