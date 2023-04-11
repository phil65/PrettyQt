"""Provides QtHelp classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtHelp import *
elif PYSIDE6:
    from PySide6.QtHelp import *
else:
    raise PythonQtError("No Qt bindings could be found")
