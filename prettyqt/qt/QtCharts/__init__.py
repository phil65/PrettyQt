"""Provides QtCharts classes and functions."""

from typing import TYPE_CHECKING

from prettyqt.qt import PYQT6, PYSIDE6


# Type checkers see PySide6 only (see prettyqt/qt/__init__.py).
if TYPE_CHECKING:
    from PySide6.QtCharts import *
elif PYQT6:
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
