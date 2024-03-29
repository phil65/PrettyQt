"""Provides QtStateMachine classes and functions."""

from prettyqt.qt import PYSIDE6


# elif PYQT6:
#     from PyQt6.QtStateMachine import *
if PYSIDE6:
    from PySide6.QtStateMachine import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
