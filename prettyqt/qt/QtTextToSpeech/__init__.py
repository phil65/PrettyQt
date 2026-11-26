"""Provides QtTextToSpeech classes and functions."""

from typing import TYPE_CHECKING

from prettyqt.qt import PYQT6, PYSIDE6


# Type checkers see PySide6 only (see prettyqt/qt/__init__.py).
if TYPE_CHECKING:
    from PySide6.QtTextToSpeech import *
elif PYQT6:
    from PyQt6.QtTextToSpeech import *
elif PYSIDE6:
    from PySide6.QtTextToSpeech import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
