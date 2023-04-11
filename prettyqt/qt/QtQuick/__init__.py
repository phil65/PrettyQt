"""Provides QtQuick classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtQuick import *
elif PYSIDE6:
    from PySide6.QtQuick import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
