"""Provides QtTest classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtTest import *
elif PYQT6:
    from PyQt6.QtTest import *
elif PYSIDE2:
    from PySide2.QtTest import *
elif PYSIDE6:
    from PySide6.QtTest import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
