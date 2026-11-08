# 🌿 xtree

[![Python 3.x](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#prerequisites)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)](#installation)

> **eXtended Tree CLI** — A lightweight, modern directory tree visualizer and project inspector.  
> Zero third-party dependencies. Built purely with Python 3.

```text
my-project/
├── src/
│   ├── api/
│   │   ├── auth.py         [ 3.4 KB]
│   │   └── routes.py       [ 8.1 KB]
│   ├── config.py           [ 1.2 KB]
│   └── main.py             [ 5.6 KB]
├── tests/
│   ├── __init__.py         [   0  B]
│   └── test_api.py         [ 2.8 KB]
├── README.md               [ 4.2 KB]
└── pyproject.toml          [ 890  B]

📊 Summary: 4 directories, 7 files, Total Size: 26.2 KB
```

---

## ⚡ Why xtree?

Standard `tree` commands on Windows and UNIX are either missing, hard to configure, or dump unwanted clutter (`.git`, `node_modules`, `__pycache__`). 

**xtree** gives you a modern, clean, and customizable alternative:
- **Zero Dependencies**: Pure Python 3 standard library. No `pip install` required.
- **Smart Filtering**: Ignores `.git`, `node_modules`, `venv`, `__pycache__`, and temporary build files out of the box.
- **Human-Readable File Sizes**: View exact sizes per file and total project footprint (`-s`).
- **Markdown & JSON Export**: One-click export for documentation or API inspection (`--markdown`, `--json`).
- **Color-Coded File Types**: Syntax-highlighted entries by extension (Python, JavaScript, Markdown, configs, etc.).
- **Depth Limiting**: Easily truncate deep hierarchies (`-L 2`).

---

## 🚀 Quick Start

### 1. Direct Execution
Clone the repository and run directly:
```bash
git clone https://github.com/otengedward882-cmd/xtree.git
cd xtree
python xtree.py
```

### 2. Make it a Global Command (Windows)
Add the folder containing `xtree.py` to your User `PATH`, or create an alias in your PowerShell profile:
```powershell
Set-Alias xtree "python C:\path\to\xtree\xtree.py"
```

---

## 📖 Command-Line Options

| Flag | Short | Description |
|---|---|---|
| `--depth <N>` | `-L` | Limit traversal to `<N>` directory levels |
| `--sizes` | `-s` | Show human-readable file sizes (`KB`, `MB`, etc.) |
| `--all` | `-a` | Show hidden files (files starting with `.`) |
| `--dirs-only` | `-d` | List directories only, omitting files |
| `--pattern <GLOB>` | `-p` | Filter files matching pattern (e.g. `*.py`, `*.json`) |
| `--ignore <NAMES>` | `-i` | Extra file or folder names to ignore |
| `--markdown` | | Output structure wrapped in a Markdown code fence |
| `--json` | | Output hierarchy as structured JSON |
| `--ascii` | | Use ASCII characters (`+--`, `|`) instead of Unicode |
| `--no-color` | | Disable ANSI terminal colors |
| `--version` | `-v` | Show version information |

---

## 💡 Practical Examples

### 1. Inspect Project (Depth 2 with File Sizes)
```bash
python xtree.py -s -L 2
```

### 2. Generate Markdown for a Documentation README
Generate a clean code block and pipe directly into your clipboard or file:
```bash
python xtree.py -s --markdown > structure.md
```

### 3. Filter for Python Files Only
```bash
python xtree.py -p "*.py"
```

### 4. Inspect as Structured JSON
```bash
python xtree.py --json
```

---

## 🐍 Python API Usage

You can also import and use `xtree` directly in your Python code:

```python
from xtree import XTree

# Initialize inspector
tree = XTree(root_dir=".", max_depth=2, show_sizes=True)

# Render formatted tree string
print(tree.render())

# Or get as JSON dictionary
json_data = tree.to_json()
```

---

## 🧪 Running Tests

The test suite runs with standard library `unittest`:
```bash
python -m unittest discover tests
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
