"""CLI helper to find missing module, class, and function docstrings."""

import ast
import os
import sys
from typing import Dict, List


SKIP_DIRS = {"venv", "node_modules"}


def find_python_files(base_dir: str) -> List[str]:
    """Yield all .py files under base_dir, skipping unwanted directories."""
    python_files = []
    for root, dirs, files in os.walk(base_dir):
        # Prune directories we do not want to descend into.
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            if filename.endswith(".py"):
                python_files.append(os.path.join(root, filename))
    return python_files


def check_docstrings(file_path: str) -> List[str]:
    """Return a list of docstring problems for the given Python file."""
    issues = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=file_path)
    except (SyntaxError, OSError) as exc:
        issues.append(f"Could not parse file: {exc}")
        return issues

    if not ast.get_docstring(tree):
        issues.append("Missing module docstring")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not ast.get_docstring(node):
                issues.append(f"Missing docstring for function `{node.name}` at line {node.lineno}")
        elif isinstance(node, ast.ClassDef):
            if not ast.get_docstring(node):
                issues.append(f"Missing docstring for class `{node.name}` at line {node.lineno}")
    return issues


def main() -> int:
    """Scan the current working tree for Python files missing docstrings."""
    base_dir = os.getcwd()
    python_files = find_python_files(base_dir)
    missing: Dict[str, List[str]] = {}

    for path in python_files:
        issues = check_docstrings(path)
        if issues:
            missing[path] = issues

    if missing:
        print("Missing docstrings detected:")
        for path, issues in sorted(missing.items()):
            print(f"{path}:")
            for issue in issues:
                print(f"  - {issue}")
        return 1

    print("All modules, functions, and classes have docstrings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
