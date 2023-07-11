"""Provides QtStateMachine classes and functions."""

from prettyqt.qt import PYQT6


if PYQT6:
    from PyQt6.Qsci import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
