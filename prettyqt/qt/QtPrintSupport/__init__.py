"""Provides QtPrintSupport classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    from PyQt6.QtPrintSupport import *
elif PYSIDE6:
    from PySide6.QtPrintSupport import *  # type: ignore
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
