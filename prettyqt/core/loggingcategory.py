from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


MSG_TYPE = bidict(
    critical=QtCore.QtMsgType.QtCriticalMsg,
    debug=QtCore.QtMsgType.QtDebugMsg,
    info=QtCore.QtMsgType.QtInfoMsg,
    warning=QtCore.QtMsgType.QtWarningMsg,
)

MsgTypeStr = Literal["critical", "debug", "info", "warning"]


class LoggingCategory(QtCore.QLoggingCategory):
    def get_level(self) -> MsgTypeStr:
        if self.isDebugEnabled():
            return "debug"
        elif self.isInfoEnabled():
            return "info"
        elif self.isWarningEnabled():
            return "warning"
        elif self.isCriticalEnabled():
            return "critical"
        else:
            return None

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
