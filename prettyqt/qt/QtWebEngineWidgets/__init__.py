"""Provides widgets to embed browser components in the user interface."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    from PyQt6.QtWebEngineWidgets import *
elif PYSIDE6:
    from PySide6.QtWebEngineWidgets import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
