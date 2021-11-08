"""Module containing helper functions."""

from __future__ import annotations

import collections
import logging
import sys
import traceback

from prettyqt import qt, widgets
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)

LOG_MAP = {
    QtCore.QtMsgType.QtInfoMsg: 20,
    QtCore.QtMsgType.QtWarningMsg: 30,
    QtCore.QtMsgType.QtCriticalMsg: 40,
    QtCore.QtMsgType.QtFatalMsg: 50,
}


def qt_message_handler(mode: QtCore.QtMsgType, context, message: str):
    level = LOG_MAP.get(mode, 20)
    logger.log(level, f"{message} ({context.file}:{context.line}, {context.file})")


def install_exceptionhook(debug: bool = False):
    def handleException(exc_type, exc_value, exc_traceback):
        """Causes the application to quit in case of an unhandled exception.

        Shows an error dialog before quitting when not in debugging mode.
        """
        logger.critical(
            f"Bug: uncaught {exc_type.__name__}",
            exc_info=(exc_type, exc_value, exc_traceback),
        )
        if debug:
            sys.exit(1)
        else:
            from prettyqt import widgets

            # Constructing a QApplication in case this hasn't been done yet.
            _ = widgets.app()
            lst = traceback.format_exception(exc_type, exc_value, exc_traceback)
            msg_box = widgets.MessageBox(
                icon="warning",
                text=f"Bug: uncaught {exc_type.__name__}",
                informative_text=str(exc_value),
                details="".join(lst),
            )
            msg_box.main_loop()
            sys.exit(1)

    sys.excepthook = handleException


def count_objects():
    win = widgets.Application.get_mainwindow()
    objects = win.findChildren(QtCore.QObject)
    counter = collections.Counter([type(o) for o in objects])
    logger.info(counter)


def is_deleted(obj) -> bool:
    if qt.API == "pyside2":
        import shiboken2

        return not shiboken2.isValid(obj)
    elif qt.API == "pyside6":
        import shiboken6

        return not shiboken6.isValid(obj)
    elif qt.API == "pyqt5":
        try:
            from PyQt5 import sip
        except ImportError:
            import sip  # type: ignore[import, no-redef]
        return sip.isdeleted(obj)
    else:
        try:
            from PyQt6 import sip
        except ImportError:
            import sip  # type: ignore[import, no-redef]
        return sip.isdeleted(obj)
