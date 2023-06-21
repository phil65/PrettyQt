from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


TYPE = bidict(
    read=QtCore.QSocketNotifier.Type.Read,
    write=QtCore.QSocketNotifier.Type.Write,
    exception=QtCore.QSocketNotifier.Type.Exception,
)

TypeStr = Literal["read", "write", "exception"]


class SocketNotifier(core.ObjectMixin, QtCore.QSocketNotifier):
    # def __repr__(self):
    #     return f"{type(self).__name__}({self.socket()}, {self.type()})"

    def get_type(self) -> TypeStr:
        """Return socket event type.

        Returns:
            socket event type
        """
        return TYPE.inverse[self.type()]


if __name__ == "__main__":
    app = core.app()
    import os

    read, write = os.pipe()
    notifier = SocketNotifier(read, QtCore.QSocketNotifier.Type.Read)
    app.exec()
