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

QtCore.QSocketNotifier.__bases__ = (core.Object,)


class SocketNotifier(QtCore.QSocketNotifier):
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

    print("hre")
    read, write = os.pipe()
    notifier = SocketNotifier(read, QtCore.QSocketNotifier.Type.Read)
    print(repr(notifier))
    app.main_loop()
