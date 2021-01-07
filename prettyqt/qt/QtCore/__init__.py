"""Provides QtCore classes and functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt.qt import PYQT5, PYSIDE2, PYSIDE6, PythonQtError

if TYPE_CHECKING:
    import datetime


if PYQT5:
    from PyQt5.QtCore import (
        QT_VERSION_STR,
        QT_VERSION_STR as __version__,
        QDateTime,
        QDate,
        QTime,
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

    def to_datetime(self) -> datetime.datetime:
        return self.toPyDateTime()

    QDateTime.toPython = to_datetime

    def to_date(self) -> datetime.date:
        return self.toPyDate()

    QDate.toPython = to_date

    def to_time(self) -> datetime.time:
        return self.toPyTime()

    QTime.toPython = to_time

    # Those are imported from `import *`
    del pyqtSignal, pyqtBoundSignal, pyqtSlot, pyqtProperty, QT_VERSION_STR
elif PYSIDE2:
    from PySide2.QtCore import *
    from PySide2.QtCore import __version__  # type: ignore
elif PYSIDE6:
    from PySide6.QtCore import *  # type: ignore
    from PySide6.QtCore import __version__  # type: ignore
