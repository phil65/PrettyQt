"""Provides QtBluetooth classes and functions."""

from prettyqt.qt import PYSIDE6


if PYSIDE6:
    from PySide6.QtBluetooth import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
