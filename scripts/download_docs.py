# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "prettyqt",
#   "pyside6",
#   "bs4",
#   "requests"
# ]
# ///


import inspect
import logging
import pathlib
from typing import Any

from bs4 import BeautifulSoup
import requests

from prettyqt.qt import QtCore, QtGui, QtWidgets


# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Define modules to scrape
MODULE_DICT: dict[str, Any] = {"QtWidgets": QtWidgets, "QtGui": QtGui, "QtCore": QtCore}


def get_class_description(module_name: str, class_name: str) -> str | None:
    """Scrape and return the detailed description of a PySide6 class.

    Args:
        module_name: The name of the module (e.g., 'QtWidgets').
        class_name: The name of the class (e.g., 'QAbstractItemView').

    Returns:
        The detailed description as a string, or None if not found.
    """
    url = f"https://doc.qt.io/qtforpython-6/PySide6/{module_name}/{class_name}.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        description_section = soup.find(id="detailed-description")
        if description_section is None:
            return None

        reference = description_section.find(class_="reference internal")
        if reference is None:
            return None

        text = reference.parent.get_text()
        return text.encode("cp1252", errors="ignore").decode(errors="ignore")
    except requests.RequestException:
        logger.exception("Error fetching %s", url)
        return None


def process_module(module_name: str, module: Any, save: bool = False) -> None:
    """Process all classes in a given module.

    Args:
        module_name: The name of the module.
        module: The module object.
        save: whether to save the docs on disk
    """
    for class_name, _ in inspect.getmembers(module, inspect.isclass):
        description = get_class_description(module_name, class_name)
        if description:
            logger.warning("%s.%s: %s", module_name, class_name, description)
            if save:
                save_path = pathlib.Path(module_name)
                save_path.mkdir(parents=True, exist_ok=True)
                (save_path / f"{class_name}.txt").write_text(description)


def main() -> None:
    """Main function to process all modules and classes."""
    for module_name, module in MODULE_DICT.items():
        process_module(module_name, module, save=True)


if __name__ == "__main__":
    main()
