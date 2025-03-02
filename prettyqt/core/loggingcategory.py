from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


MsgTypeStr = Literal["critical", "debug", "info", "warning", "fatal"]

MSG_TYPE: bidict[MsgTypeStr, QtCore.QtMsgType] = bidict(
    critical=QtCore.QtMsgType.QtCriticalMsg,
    debug=QtCore.QtMsgType.QtDebugMsg,
    info=QtCore.QtMsgType.QtInfoMsg,
    warning=QtCore.QtMsgType.QtWarningMsg,
)


class LoggingCategory(QtCore.QLoggingCategory):
    """Represents a category, or 'area' in the logging infrastructure."""

    def get_level(self) -> MsgTypeStr:
        if self.isDebugEnabled():
            return "debug"
        if self.isInfoEnabled():
            return "info"
        if self.isWarningEnabled():
            return "warning"
        if self.isCriticalEnabled():
            return "critical"
        return "fatal"

    def set_enabled(
        self,
        level: MsgTypeStr,
    ):
        self.setEnabled(MSG_TYPE[level], True)

    def set_disabled(self, level: MsgTypeStr):
        self.setEnabled(MSG_TYPE[level], False)


if __name__ == "__main__":
    cat = LoggingCategory("test")
    cat.set_disabled("debug")
    print(cat.get_level())
