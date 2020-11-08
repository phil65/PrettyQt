"""Provides QtCharts classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    try:
        from PyQt5 import QtChart as QtCharts
    except ImportError:
        raise PythonQtError(
            "The QtChart module was not found. "
            "It needs to be installed separately for PyQt5."
        )
elif PYSIDE2:
    from PySide2.QtCharts import *
else:
    raise PythonQtError("No Qt bindings could be found")
