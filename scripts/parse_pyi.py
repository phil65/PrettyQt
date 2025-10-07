# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "typed_ast",
# ]
# ///

import pathlib
import sys

from typed_ast import ast3


def add_parents(tree):
    for node in ast3.walk(tree):
        for child in ast3.iter_child_nodes(node):
            child.parent = node  # type: ignore


def find_enums(tree):
    for node in ast3.walk(tree):
        if not isinstance(node, ast3.Assign):
            continue
        if node.type_comment is None:
            continue
        if "." not in node.type_comment:
            continue
        if not node.type_comment.startswith("'"):
            continue
        comment = node.type_comment.strip("'")
        mod, cls = comment.rsplit(".", maxsplit=1)
        assert len(node.targets) == 1
        name = node.targets[0].id  # type: ignore
        yield (mod, cls, name)


def main():
    for filename in sys.argv[1:]:
        tree = ast3.parse(pathlib.Path(filename).read_text("utf-8"))
        for mod, cls, name in find_enums(tree):
            old = f"{mod}.{name}"
            new = f"{mod}.{cls}.{name}"
            print(f"{old} {new}")


if __name__ == "__main__":
    main()
