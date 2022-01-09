"""Provides QtScxml classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtScxml import *
elif PYQT6:
    from PyQt6.QtScxml import *
elif PYSIDE2:
    from PySide2.QtScxml import *
elif PYSIDE6:
    from PySide6.QtScxml import *
else:
    raise PythonQtError("No Qt bindings could be found")
