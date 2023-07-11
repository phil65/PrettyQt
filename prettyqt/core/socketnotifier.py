from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


TypeStr = Literal["read", "write", "exception"]

TYPE: bidict[TypeStr, core.QSocketNotifier.Type] = bidict(
    read=core.QSocketNotifier.Type.Read,
    write=core.QSocketNotifier.Type.Write,
    exception=core.QSocketNotifier.Type.Exception,
)


class SocketNotifier(core.ObjectMixin, core.QSocketNotifier):
    """Support for monitoring activity on a file descriptor."""

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
    notifier = SocketNotifier(read, core.QSocketNotifier.Type.Read)
    app.exec()
