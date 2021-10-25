"""Provides QtWidgets classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtWidgets import *
elif PYSIDE2:
    from PySide2.QtWidgets import *
elif PYQT6:
    from PyQt6.QtWidgets import *  # type: ignore
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget  # type: ignore
    from PyQt6.QtGui import (  # type: ignore
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
    QMenu.exec_ = QMenu.exec  # type: ignore
elif PYSIDE6:
    from PySide6.QtWidgets import *  # type: ignore
    from PySide6.QtOpenGLWidgets import QOpenGLWidget  # type: ignore
    from PySide6.QtGui import (  # type: ignore
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
