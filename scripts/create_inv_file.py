# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "sphinx",
#   "pyside6"
# ]
# ///

import codecs
import pathlib
import re
import sys
import zlib

import PySide6
import requests
from sphinx.ext.intersphinx import inspect_main
from sphinx.util.inventory import InventoryFileReader


PYSIDE_URI = "https://doc.qt.io/qtforpython/"
PACKAGE_NAME = "PySide6"

# File paths
ORIGINAL_INV = pathlib.Path("qt6-original.inv")
ORIGINAL_TXT = pathlib.Path("qt6-original.txt")
MODIFIED_INV = pathlib.Path("qt6-with-aliases.inv")
MODIFIED_TXT = pathlib.Path("qt6-with-aliases.txt")


def get_alias_modules() -> list[str]:
    """Get a list of all Qt modules.

    Returns:
        A list of Qt module names.
    """
    return PySide6.__all__


def download_original_inv(url: str, output_path: pathlib.Path) -> None:
    """Download the original objects.inv file.

    Args:
        url: The URL to download the inventory file from.
        output_path: The path to save the downloaded file.
    """
    response = requests.get(url)
    response.raise_for_status()
    output_path.write_bytes(response.content)


def parse_inventory_line(line: str) -> tuple[str, str, str, str, str]:
    """Parse a line from the inventory file.

    Args:
        line: A line from the inventory file.

    Returns:
        A tuple containing (name, type, priority, location, display_name).
    """
    match = re.match(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)", line.rstrip())
    if not match:
        raise ValueError(f"Invalid inventory line: {line}")
    return match.groups()


def generate_aliases(module: str, classname: str, method: str) -> list[str]:
    """Generate aliases for a given class and method.

    Args:
        module: The Qt module name.
        classname: The class name.
        method: The method name (can be empty).

    Returns:
        A list of generated aliases.
    """
    return [
        f"PyQt6.{module}.{classname}{method}",
        f"prettyqt.qt.{module}.{classname}{method}",
        f"prettyqt.{module[2:].lower()}.{classname}{method}",
        f"qtpy.{module}.{classname}{method}",
        f"PySide6.{module}.{classname}{method}",
        f"{module}.{classname}{method}",
        f"{classname}{method}",
    ]


def create_modified_inv(
    original_path: pathlib.Path,
    modified_path: pathlib.Path,
    alias_modules: list[str],
) -> None:
    """Create a modified inventory file with aliases.

    Args:
        original_path: Path to the original inventory file.
        modified_path: Path to save the modified inventory file.
        alias_modules: List of Qt modules to generate aliases for.
    """
    with original_path.open("rb") as fin, modified_path.open("wb") as fout:
        compressor = zlib.compressobj(9)
        reader = InventoryFileReader(fin)

        def write(*args: str) -> None:
            fout.write(compressor.compress((" ".join(args) + "\n").encode("utf-8")))

        # Copy the header
        for _ in range(4):
            fout.write((reader.readline() + "\n").encode("utf-8"))

        for line in reader.read_compressed_lines():
            name, typ, prio, location, dispname = parse_inventory_line(line)
            location = location.rstrip("$") + name

            write(name, typ, prio, location, dispname)
            if name.endswith("QtCore.Signal"):
                write(
                    f"{PACKAGE_NAME}.QtCore.SignalInstance", typ, prio, location, dispname
                )

            # Apply the aliases
            for module in alias_modules:
                match = re.match(
                    rf"{PACKAGE_NAME}\.{module}\.{PACKAGE_NAME}\.{module}\.(\w+)(\.\w+)?",
                    name,
                )
                if match:
                    classname, method = match.groups()
                    method = method or ""
                    for alias in generate_aliases(module, classname, method):
                        write(alias, typ, prio, location, dispname)

        fout.write(compressor.flush())


def inspect_inventory(inv_path: pathlib.Path, output_path: pathlib.Path) -> None:
    """Inspect an inventory file and save the output to a text file.

    Args:
        inv_path: Path to the inventory file to inspect.
        output_path: Path to save the inspection output.
    """
    with codecs.open(output_path, "wb", encoding="utf-8") as f:
        sys.stdout = f
        inspect_main([str(inv_path)])
    sys.stdout = sys.__stdout__


def main() -> None:
    """Main function to orchestrate the inventory file creation and inspection."""
    alias_modules = get_alias_modules()
    download_original_inv(f"{PYSIDE_URI}objects.inv", ORIGINAL_INV)
    create_modified_inv(ORIGINAL_INV, MODIFIED_INV, alias_modules)

    inspect_inventory(ORIGINAL_INV, ORIGINAL_TXT)
    inspect_inventory(MODIFIED_INV, MODIFIED_TXT)

    print("Created:")
    print(f"  {ORIGINAL_INV}")
    print(f"  {ORIGINAL_TXT}")
    print(f"  {MODIFIED_INV}")
    print(f"  {MODIFIED_TXT}")


if __name__ == "__main__":
    main()
