"""Provides QtHelp classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtHelp import *
elif PYQT6:
    from PyQt6.QtHelp import *
elif PYSIDE2:
    from PySide2.QtHelp import *
elif PYSIDE6:
    from PySide6.QtHelp import *
else:
    raise PythonQtError("No Qt bindings could be found")
