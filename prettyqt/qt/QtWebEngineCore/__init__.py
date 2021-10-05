"""Provides QtWebEngineCore classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtWebEngineCore import *
elif PYSIDE2:
    from PySide2.QtWebEngineCore import *
elif PYQT6:
    from PyQt6.QtWebEngineCore import *
elif PYSIDE6:
    from PySide6.QtWebEngineCore import *
else:
    raise PythonQtError("No Qt bindings could be found")
