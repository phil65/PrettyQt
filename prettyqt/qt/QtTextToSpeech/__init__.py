"""Provides QtTextToSpeech classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    from PyQt5.QtTextToSpeech import *
elif PYSIDE2:
    from PySide2.QtTextToSpeech import *
else:
    raise PythonQtError("No Qt bindings could be found")
