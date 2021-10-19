"""Provides QtStateMachine classes and functions."""

from prettyqt.qt import PYQT5, PYQT6, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtCore import (
        QAbstractState,
        QAbstractTransition,
        QEventTransition,
        QFinalState,
        QHistoryState,
        QSignalTransition,
        QState,
        QStateMachine,
    )
    from PyQt5.QtWidgets import QKeyEventTransition, QMouseEventTransition
# elif PYQT6:
#     from PyQt6.QtStateMachine import *
elif PYSIDE2:
    from PySide2.QtCore import (
        QAbstractState,
        QAbstractTransition,
        QEventTransition,
        QFinalState,
        QHistoryState,
        QSignalTransition,
        QState,
        QStateMachine,
    )
    from PySide2.QtWidgets import QKeyEventTransition, QMouseEventTransition
elif PYSIDE6:
    from PySide6.QtStateMachine import *
else:
    raise PythonQtError("No Qt bindings could be found")
