"""Provides QtTest classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5 import uic

    class QUiLoader:
        def load(self, path: str):
            return uic.loadUi(path)


elif PYSIDE2:
    from PySide2.QtUiTools import QUiLoader
elif PYSIDE6:
    from PySide6.QtUiTools import QUiLoader  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
