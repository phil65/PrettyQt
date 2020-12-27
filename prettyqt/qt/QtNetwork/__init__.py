"""Provides QtNetwork classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtNetwork import *
elif PYSIDE2:
    from PySide2.QtNetwork import *
elif PYSIDE6:
    from PySide6.QtNetwork import *  # type: ignore
else:
    raise PythonQtError("No Qt bindings could be found")
