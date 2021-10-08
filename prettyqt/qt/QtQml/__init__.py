"""Provides QtQml classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtQml import *
elif PYQT6:
    from PyQt6.QtQml import *
elif PYSIDE2:
    from PySide2.QtQml import *
elif PYSIDE6:
    from PySide6.QtQml import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
