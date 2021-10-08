"""Provides QtWidgets classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtWidgets import *
elif PYSIDE2:
    from PySide2.QtWidgets import *
elif PYQT6:
    from PyQt6.QtWidgets import *  # type: ignore
    from PyQt6.QtGui import (  # type: ignore
        QAction,
        QActionGroup,
        QUndoCommand,
        QUndoStack,
        QUndoGroup,
        QShortcut,
        QFileSystemModel,
    )
elif PYSIDE6:
    from PySide6.QtWidgets import *  # type: ignore
    from PySide6.QtGui import (  # type: ignore
        QAction,
        QActionGroup,
        QUndoCommand,
        QUndoStack,
        QUndoGroup,
        QShortcut,
    )
else:
    raise PythonQtError("No Qt bindings could be found")
