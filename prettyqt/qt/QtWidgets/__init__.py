"""Provides QtWidgets classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtWidgets import *
elif PYSIDE2:
    from PySide2.QtWidgets import *
elif PYSIDE6:
    from PySide6.QtWidgets import *
    from PySide6.QtGui import (  # type: ignore
        QAction,
        QActionGroup,
        QUndoCommand,
        QUndoStack,
        QUndoGroup,
    )
else:
    raise PythonQtError("No Qt bindings could be found")
