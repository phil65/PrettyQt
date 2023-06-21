from __future__ import annotations

import contextlib
import logging

from prettyqt.qt import QtCore


LOG_MAP = {
    QtCore.QtMsgType.QtDebugMsg: logging.DEBUG,
    QtCore.QtMsgType.QtInfoMsg: logging.INFO,
    QtCore.QtMsgType.QtWarningMsg: logging.WARNING,
    QtCore.QtMsgType.QtCriticalMsg: logging.ERROR,
    QtCore.QtMsgType.QtFatalMsg: logging.CRITICAL,
    QtCore.QtMsgType.QtSystemMsg: logging.CRITICAL,
}

logger = logging.getLogger(__name__)

# qFormatLogMessage(QtMsgType type, const QMessageLogContext context, const QString str)
# qInstallMessageHandler(QtMessageHandler handler)
# qSetMessagePattern(const QString &pattern)


class MessageHandler:
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._previous_handler = None

    def install(self):
        self._previous_handler = QtCore.qInstallMessageHandler(self)

    def uninstall(self):
        if self._previous_handler is None:
            QtCore.qInstallMessageHandler(self._previous_handler)

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, *args):
        self.uninstall()

    def __call__(
        self,
        msgtype: QtCore.QtMsgType,
        context: QtCore.QMessageLogContext,
        message: str,
    ):
        ctx = dict.fromkeys(["category", "file", "function", "line"])
        with contextlib.suppress(UnicodeDecodeError):
            ctx["category"] = context.category
        with contextlib.suppress(UnicodeDecodeError):
            ctx["file"] = context.file
        with contextlib.suppress(UnicodeDecodeError):
            ctx["function"] = context.function
        with contextlib.suppress(UnicodeDecodeError):
            ctx["line"] = context.line

        level = LOG_MAP[msgtype]
        self._logger.log(level, message, extra=ctx)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    handler = MessageHandler(logger)
    with app.debug_mode():
        app.exec()
