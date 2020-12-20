"""Provides QtCore classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError


if PYQT5:
    from PyQt5.QtCore import (
        QT_VERSION_STR,
        QT_VERSION_STR as __version__,
        QDateTime,
        pyqtBoundSignal,
        pyqtBoundSignal as SignalInstance,
        pyqtProperty,
        pyqtProperty as Property,
        pyqtSignal,
        pyqtSignal as Signal,
        pyqtSlot,
        pyqtSlot as Slot,
    )

    # For issue #153
    from PyQt5.QtCore import *

    QDateTime.toPython = QDateTime.toPyDateTime

    # Those are imported from `import *`
    del pyqtSignal, pyqtBoundSignal, pyqtSlot, pyqtProperty, QT_VERSION_STR
elif PYSIDE2:
    from PySide2.QtCore import *
    from PySide2.QtCore import __version__  # type: ignore
elif PYSIDE6:
    from PySide6.QtCore import *
    from PySide6.QtCore import __version__  # type: ignore
