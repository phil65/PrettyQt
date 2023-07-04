from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.utils import bidict


SocketError = bluetooth.QBluetoothSocket.SocketError

SocketErrorStr = Literal[
    "unknown_socket",
    "no_socket",
    "host_not_found",
    "service_not_found",
    "network",
    "unsupported_protocol",
    "operation",
    "remote_host_closed",
    "missing_permissions",
]

SOCKET_ERROR: bidict[SocketErrorStr, SocketError] = bidict(
    unknown_socket=SocketError.UnknownSocketError,
    no_socket=SocketError.NoSocketError,
    host_not_found=SocketError.HostNotFoundError,
    service_not_found=SocketError.ServiceNotFoundError,
    network=SocketError.NetworkError,
    unsupported_protocol=SocketError.UnsupportedProtocolError,
    operation=SocketError.OperationError,
    remote_host_closed=SocketError.RemoteHostClosedError,
    missing_permissions=SocketError.MissingPermissionsError,
)


SocketState = bluetooth.QBluetoothSocket.SocketState
SocketStateStr = Literal[
    "unconnected",
    "service_lookup",
    "connecting",
    "connected",
    "bound",
    "closing",
    "listening",
]

SOCKET_STATE: bidict[SocketStateStr, SocketState] = bidict(
    unconnected=SocketState.UnconnectedState,
    service_lookup=SocketState.ServiceLookupState,
    connecting=SocketState.ConnectingState,
    connected=SocketState.ConnectedState,
    bound=SocketState.BoundState,
    closing=SocketState.ClosingState,
    listening=SocketState.ListeningState,
)


class BluetoothSocket(core.IODeviceMixin, bluetooth.QBluetoothSocket):
    def __init__(
        self,
        protocol: bluetooth.bluetoothserviceinfo.ProtocolStr
        | bluetooth.QBluetoothServiceInfo.Protocol,
        parent: core.QObject | None = None,
    ):
        protocol = bluetooth.bluetoothserviceinfo.PROTOCOL.get_enum_value(protocol)
        super().__init__(protocol, parent)

    def get_error(self) -> SocketErrorStr:
        return SOCKET_ERROR.inverse[self.error()]

    def get_state(self) -> SocketStateStr:
        return SOCKET_STATE.inverse[self.state()]

    def get_local_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.localAddress())

    def get_peer_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.peerAddress())

    def get_socket_type(self) -> bluetooth.bluetoothserviceinfo.ProtocolStr:
        return bluetooth.bluetoothserviceinfo.PROTOCOL.inverse[self.socketType()]


if __name__ == "__main__":
    from prettyqt import core

    app = core.app()
    socket = BluetoothSocket("l2_cap")
    with app.debug_mode():
        app.exec()
