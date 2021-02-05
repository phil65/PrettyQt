from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.qt import QtNetwork
from prettyqt.utils import InvalidParamError, bidict, helpers


SOCKET_OPTION = bidict(
    none=QtNetwork.QLocalServer.SocketOption(),  # NoOptions
    user=QtNetwork.QLocalServer.UserAccessOption,
    group=QtNetwork.QLocalServer.GroupAccessOption,
    other=QtNetwork.QLocalServer.OtherAccessOption,
    world=QtNetwork.QLocalServer.WorldAccessOption,
)

SocketOptionStr = Literal["none", "user", "group", "other", "world"]

QtNetwork.QLocalServer.__bases__ = (core.Object,)


class LocalServer(QtNetwork.QLocalServer):
    def get_server_error(self) -> network.abstractsocket.SocketErrorStr:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]

    def set_socket_options(self, *name: SocketOptionStr):
        for item in name:
            if item not in SOCKET_OPTION:
                raise InvalidParamError(item, SOCKET_OPTION)
        flags = helpers.merge_flags(name, SOCKET_OPTION)
        self.setSocketOptions(flags)

    def get_socket_options(self) -> list[SocketOptionStr]:
        return [k for k, v in SOCKET_OPTION.items() if v & self.socketOptions()]


if __name__ == "__main__":
    server = LocalServer()
