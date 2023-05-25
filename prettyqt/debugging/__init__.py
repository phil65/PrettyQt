"""debugging pachakge."""

from .stalker import Stalker
from .tracebackdialog import TracebackDialog
from .errormessagebox import ErrorMessageBox
from .messagehandler import MessageHandler


import logging
from prettyqt import qt
from prettyqt.qt import QtCore


class QtLogger(logging.Handler):
    def emit(self, record: logging.LogRecord):
        match record.level:
            case logging.DEBUG:
                QtCore.qDebug(self.format(record))
            case logging.INFO:
                QtCore.qInfo(self.format(record))
            case logging.WARNING:
                QtCore.qWarning(self.format(record))
            case logging.CRITICAL:
                QtCore.qCritical(self.format(record))
            case logging.CRITICAL:
                QtCore.qFatal(self.format(record))


def is_deleted(obj) -> bool:
    match qt.API:
        case "pyside6":
            import shiboken6

            return not shiboken6.isValid(obj)
        case "pyqt6":
            from PyQt6 import sip

            return sip.isdeleted(obj)


__all__ = ["Stalker", "TracebackDialog", "ErrorMessageBox", "MessageHandler"]
