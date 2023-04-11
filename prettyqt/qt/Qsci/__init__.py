"""Provides QtStateMachine classes and functions."""

from prettyqt.qt import PYQT6, PythonQtError


if PYQT6:
    from PyQt6.Qsci import *
else:
    raise PythonQtError("No Qt bindings could be found")
