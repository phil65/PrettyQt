from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.utils import bidict


SOCKET_OPTION = bidict(
    none=network.QLocalServer.SocketOption(0),
    user=network.QLocalServer.SocketOption.UserAccessOption,
    group=network.QLocalServer.SocketOption.GroupAccessOption,
    other=network.QLocalServer.SocketOption.OtherAccessOption,
    world=network.QLocalServer.SocketOption.WorldAccessOption,
)

SocketOptionStr = Literal["none", "user", "group", "other", "world"]


class LocalServer(core.ObjectMixin, network.QLocalServer):
    """Local socket based server."""

    def get_server_error(self) -> network.abstractsocket.SocketErrorStr:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]

    def set_socket_options(self, *name: SocketOptionStr):
        flags = SOCKET_OPTION.merge_flags(name)
        self.setSocketOptions(flags)

    def get_socket_options(self) -> list[SocketOptionStr]:
        return SOCKET_OPTION.get_list(self.socketOptions())


if __name__ == "__main__":
    server = LocalServer()
