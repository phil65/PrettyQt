"""Provides QtNetwork classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    from PyQt6.QtNetwork import *
elif PYSIDE6:
    from PySide6.QtNetwork import *  # type: ignore
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
