from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtNetwork
from prettyqt.utils import InvalidParamError, bidict


mod = QtNetwork.QLocalSocket

LOCAL_SOCKET_ERROR = bidict(
    connection_refused=mod.LocalSocketError.ConnectionRefusedError,
    peer_closed=mod.LocalSocketError.PeerClosedError,
    server_not_found=mod.LocalSocketError.ServerNotFoundError,
    socket_access=mod.LocalSocketError.SocketAccessError,
    socket_resource=mod.LocalSocketError.SocketResourceError,
    socket_timeout=mod.LocalSocketError.SocketTimeoutError,
    datagram_too_large=mod.LocalSocketError.DatagramTooLargeError,
    connection=mod.LocalSocketError.ConnectionError,
    unsupported_socket_operation=mod.LocalSocketError.UnsupportedSocketOperationError,
    operation=mod.LocalSocketError.OperationError,
    unknown_socket=mod.LocalSocketError.UnknownSocketError,
)

LocalSocketErrorStr = Literal[
    "connection_refused",
    "peer_closed",
    "server_not_found",
    "socket_access",
    "socket_resource",
    "socket_timeout",
    "datagram_too_large",
    "connection",
    "unsupported_socket_operation",
    "operation",
    "unknown_socket",
]

LOCAL_SOCKET_STATE = bidict(
    unconnected=mod.LocalSocketState.UnconnectedState,
    connecting=mod.LocalSocketState.ConnectingState,
    connected=mod.LocalSocketState.ConnectedState,
    closing=mod.LocalSocketState.ClosingState,
)

LocalSocketStateStr = Literal[
    "unconnected",
    "connecting",
    "connected",
    "closing",
]


QtNetwork.QLocalSocket.__bases__ = (core.IODevice,)


class LocalSocket(QtNetwork.QLocalSocket):
    def __bool__(self):
        return self.isValid()

    def get_error(self) -> LocalSocketErrorStr:
        return LOCAL_SOCKET_ERROR.inverse[self.error()]

    def get_state(self) -> LocalSocketStateStr:
        return LOCAL_SOCKET_STATE.inverse[self.state()]

    def connect_to_server(
        self,
        server_name: str | None = None,
        mode: core.iodevice.OpenModeStr = "read_write",
    ):
        if mode not in core.iodevice.OPEN_MODES:
            raise InvalidParamError(mode, core.iodevice.OPEN_MODES)
        if server_name is not None:
            self.connectToServer(server_name, core.iodevice.OPEN_MODES[mode])
        else:
            self.connectToServer(core.iodevice.OPEN_MODES[mode])


if __name__ == "__main__":
    server = LocalSocket()
