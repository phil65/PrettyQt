import inspect
import pathlib

from bs4 import BeautifulSoup
import requests

from prettyqt.qt import QtCore, QtGui, QtWidgets


module_dict = dict(QtWidgets=QtWidgets, QtGui=QtGui, QtCore=QtCore)

for module_name, module in module_dict.items():
    clsmembers = inspect.getmembers(module, inspect.isclass)
    for klass_name, _klass in clsmembers:
        url = f"https://doc.qt.io/qtforpython-6/PySide6/{module_name}/{klass_name}.html"
        website = requests.get(url)
        results = BeautifulSoup(website.content, "html.parser")
        match = results.find(id="detailed-description")
        if match is None:
            continue
        text = match.get_text()
        text = text.encode("cp1252", errors="ignore")
        text = text.decode(errors="ignore")
        # try:
        #     print(text)
        # except:
        #     pass
        path = pathlib.Path() / module_name
        path.mkdir(parents=True, exist_ok=True)
        filepath = path / f"{klass_name}.txt"
        filepath.write_text(text)
        print(f"wrote to {filepath}")
