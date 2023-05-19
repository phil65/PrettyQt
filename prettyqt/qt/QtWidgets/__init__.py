"""Provides QtWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import QFileSystemModel

elif PYSIDE6:
    from PySide6.QtWidgets import *
else:
    raise PythonQtError("No Qt bindings could be found")
