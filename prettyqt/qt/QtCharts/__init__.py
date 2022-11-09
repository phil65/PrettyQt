"""Provides QtCharts classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE6, PythonQtError


if PYQT5:
    try:
        from PyQt5.QtChart import *
    except ImportError:
        raise PythonQtError(
            "The QtChart module was not found. "
            "It needs to be installed separately for PyQt5."
        )
elif PYQT6:
    try:
        from PyQt6.QtCharts import *
    except ImportError:
        raise PythonQtError(
            "The QtChart module was not found. "
            "It needs to be installed separately for PyQt6."
        )

elif PYSIDE6:
    from PySide6.QtCharts import *
else:
    raise PythonQtError("No Qt bindings could be found")
