# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


TYPE = bidict(
    read=QtCore.QSocketNotifier.Read,
    write=QtCore.QSocketNotifier.Write,
    exception=QtCore.QSocketNotifier.Exception,
)


QtCore.QSocketNotifier.__bases__ = (core.Object,)


class SocketNotifier(QtCore.QSocketNotifier):
    # def __repr__(self):
    #     return f"{type(self).__name__}({self.socket()}, {self.type()})"

    def get_type(self) -> str:
        """Return socket event type.

        Possible values: "read", "write", "exception"

        Returns:
            socket event type
        """
        return TYPE.inv[self.type()]


if __name__ == "__main__":
    app = core.app()
    import os

    print("hre")
    read, write = os.pipe()
    notifier = SocketNotifier(read, QtCore.QSocketNotifier.Read)
    print(repr(notifier))
    app.main_loop()
