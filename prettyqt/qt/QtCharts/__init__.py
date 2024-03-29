"""Provides QtCharts classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6


if PYQT6:
    try:
        from PyQt6.QtCharts import *
    except ImportError:
        raise ModuleNotFoundError(
            "The QtChart module was not found. "
            "It needs to be installed separately for PyQt6."
        )

elif PYSIDE6:
    from PySide6.QtCharts import *
else:
    raise ModuleNotFoundError("No Qt bindings could be found")
