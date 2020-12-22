"""Provides QtTest classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtTest import *
elif PYSIDE2:
    from PySide2.QtTest import *
elif PYSIDE6:
    from PySide6.QtTest import *
else:
    raise PythonQtError("No Qt bindings could be found")
