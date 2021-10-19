"""Provides QtStateMachine classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PythonQtError


if PYQT5:
    from PyQt5.Qsci import *
elif PYQT6:
    from PyQt6.Qsci import *
else:
    raise PythonQtError("No Qt bindings could be found")
