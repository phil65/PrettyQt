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

from bs4 import BeautifulSoup
import requests

from prettyqt.qt import QtCore, QtGui, QtWidgets


module_dict = dict(QtWidgets=QtWidgets, QtGui=QtGui, QtCore=QtCore)


def scrape(module_name, klass_name):
    url = f"https://doc.qt.io/qtforpython-6/PySide6/{module_name}/{klass_name}.html"
    website = requests.get(url)
    results = BeautifulSoup(website.content, "html.parser")
    match = results.find(id="detailed-description")
    # logger.warning(match)
    if match is None:
        return
    match = match.find(**{"class": "reference internal"})
    # logger.warning(match)
    if match is None:
        return
    text = match.parent.get_text()
    text = text.encode("cp1252", errors="ignore")
    text = text.decode(errors="ignore")
    logger.warning(text)
    pathlib.Path() / module_name
    # path.mkdir(parents=True, exist_ok=True)
    # filepath = path / f"{klass_name}.txt"
    # filepath.write_text(text)


logger = logging.getLogger(__name__)
for module_name, module in module_dict.items():
    clsmembers = inspect.getmembers(module, inspect.isclass)
    for klass_name, _klass in clsmembers:
        scrape(module_name, klass_name)


if __name__ == "__main__":
    scrape("QtWidgets", "QAbstractItemView")
