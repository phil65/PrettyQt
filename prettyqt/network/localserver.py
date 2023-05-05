from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.qt import QtNetwork
from prettyqt.utils import InvalidParamError, bidict


SOCKET_OPTION = bidict(
    none=QtNetwork.QLocalServer.SocketOption(0),
    user=QtNetwork.QLocalServer.SocketOption.UserAccessOption,
    group=QtNetwork.QLocalServer.SocketOption.GroupAccessOption,
    other=QtNetwork.QLocalServer.SocketOption.OtherAccessOption,
    world=QtNetwork.QLocalServer.SocketOption.WorldAccessOption,
)

SocketOptionStr = Literal["none", "user", "group", "other", "world"]


class LocalServer(core.ObjectMixin, QtNetwork.QLocalServer):
    def get_server_error(self) -> network.abstractsocket.SocketErrorStr:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]

    def set_socket_options(self, *name: SocketOptionStr):
        for item in name:
            if item not in SOCKET_OPTION:
                raise InvalidParamError(item, SOCKET_OPTION)
        flags = SOCKET_OPTION.merge_flags(name)
        self.setSocketOptions(flags)

    def get_socket_options(self) -> list[SocketOptionStr]:
        return SOCKET_OPTION.get_list(self.socketOptions())


if __name__ == "__main__":
    server = LocalServer()
