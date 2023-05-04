"""Provides QtWidgets classes and functions."""

from prettyqt.qt import PYQT6, PYSIDE6, PythonQtError


if PYQT6:
    from PyQt6.QtWidgets import *
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
    from PyQt6.QtGui import (
        QAction,
        QActionGroup,
        QUndoCommand,
        QUndoStack,
        QUndoGroup,
        QShortcut,
        QFileSystemModel,
    )

    QTextEdit.setTabStopWidth = QTextEdit.setTabStopDistance
    QTextEdit.tabStopWidth = QTextEdit.tabStopDistance
    QPlainTextEdit.setTabStopWidth = QPlainTextEdit.setTabStopDistance
    QPlainTextEdit.tabStopWidth = QPlainTextEdit.tabStopDistance
    QPlainTextEdit.print_ = lambda self, *args, **kwargs: self.print(*args, **kwargs)
    QDialog.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
    QMenu.exec_ = lambda self, *args, **kwargs: self.exec(*args, **kwargs)
elif PYSIDE6:
    from PySide6.QtWidgets import *
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
    from PySide6.QtGui import (
        QAction,
        QActionGroup,
        QUndoCommand,
        QUndoStack,
        QUndoGroup,
        QShortcut,
    )

    QTextEdit.setTabStopWidth = QTextEdit.setTabStopDistance
    QTextEdit.tabStopWidth = QTextEdit.tabStopDistance
    QPlainTextEdit.setTabStopWidth = QPlainTextEdit.setTabStopDistance
    QPlainTextEdit.tabStopWidth = QPlainTextEdit.tabStopDistance
else:
    raise PythonQtError("No Qt bindings could be found")
