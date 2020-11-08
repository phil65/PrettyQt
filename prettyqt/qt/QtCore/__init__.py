"""Provides QtCore classes and functions."""

from prettyqt.qt import PYQT5, PYSIDE2, PythonQtError


if PYQT5:
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtBoundSignal as SignalInstance
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import QT_VERSION_STR as __version__
    from PyQt5.QtCore import pyqtSignal
    from PyQt5.QtCore import pyqtBoundSignal
    from PyQt5.QtCore import pyqtSlot
    from PyQt5.QtCore import pyqtProperty
    from PyQt5.QtCore import QT_VERSION_STR

    # For issue #153
    from PyQt5.QtCore import QDateTime

    QDateTime.toPython = QDateTime.toPyDateTime

    # Those are imported from `import *`
    del pyqtSignal, pyqtBoundSignal, pyqtSlot, pyqtProperty, QT_VERSION_STR
elif PYSIDE2:
    from PySide2.QtCore import *
    from PySide2.QtCore import __version__
