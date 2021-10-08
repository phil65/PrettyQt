from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import InvalidParamError, bidict, mappers


mod = QtNetwork.QAbstractSocket

BIND_MODE = bidict(
    share_address=mod.BindFlag.ShareAddress,
    dont_share_address=mod.BindFlag.DontShareAddress,
    reuse_address_hint=mod.BindFlag.ReuseAddressHint,
    default_for_platform=mod.BindFlag.DefaultForPlatform,
)

BindModeStr = Literal[
    "share_address",
    "dont_share_address",
    "reuse_address_hint",
    "default_for_platform",
]

NETWORK_LAYER_PROTOCOL = bidict(
    ipv4=mod.NetworkLayerProtocol.IPv4Protocol,
    ipv6=mod.NetworkLayerProtocol.IPv6Protocol,
    any_ip=mod.NetworkLayerProtocol.AnyIPProtocol,
    unknown=mod.NetworkLayerProtocol.UnknownNetworkLayerProtocol,
)

NetworkLayerProtocolStr = Literal["ipv4", "ipv6", "any_ip", "unknown"]

PAUSE_MODES = mappers.FlagMap(
    mod.PauseMode,
    never=mod.PauseMode.PauseNever,
    on_ssl_errors=mod.PauseMode.PauseOnSslErrors,
)

PauseModeStr = Literal["never", "on_ssl_errors"]

mod = mod

SOCKET_ERROR = bidict(
    connection_refused=mod.SocketError.ConnectionRefusedError,
    remote_host_closed=mod.SocketError.RemoteHostClosedError,
    host_not_found=mod.SocketError.HostNotFoundError,
    socket_access=mod.SocketError.SocketAccessError,
    socket_resource=mod.SocketError.SocketResourceError,
    socket_timeout=mod.SocketError.SocketTimeoutError,
    diagram_too_large=mod.SocketError.DatagramTooLargeError,
    network=mod.SocketError.NetworkError,
    address_in_use=mod.SocketError.AddressInUseError,
    socket_address_not_available=mod.SocketError.SocketAddressNotAvailableError,
    unsupported_socket_operation=mod.SocketError.UnsupportedSocketOperationError,
    proxy_authentication_required=mod.SocketError.ProxyAuthenticationRequiredError,
    ssl_handshake_failed=mod.SocketError.SslHandshakeFailedError,
    unfinished_socket_operation=mod.SocketError.UnfinishedSocketOperationError,
    proxy_connection_refused=mod.SocketError.ProxyConnectionRefusedError,
    proxy_connection_closed=mod.SocketError.ProxyConnectionClosedError,
    proxy_connection_timeout=mod.SocketError.ProxyConnectionTimeoutError,
    proxy_not_found=mod.SocketError.ProxyNotFoundError,
    proxy_protocol=mod.SocketError.ProxyProtocolError,
    operation=mod.SocketError.OperationError,
    ssl_internal=mod.SocketError.SslInternalError,
    ssl_invalid_user_data=mod.SocketError.SslInvalidUserDataError,
    temporary=mod.SocketError.TemporaryError,
    unknown_socket=mod.SocketError.UnknownSocketError,
)

SocketErrorStr = Literal[
    "connection_refused",
    "remote_host_closed",
    "host_not_found",
    "socket_access",
    "socket_resource",
    "socket_timeout",
    "diagram_too_large",
    "network",
    "address_in_use",
    "socket_address_not_available",
    "unsupported_socket_operation",
    "proxy_authentication_required",
    "ssl_handshake_failed",
    "unfinished_socket_operation",
    "proxy_connection_refused",
    "proxy_connection_closed",
    "proxy_connection_timeout",
    "proxy_not_found",
    "proxy_protocol",
    "operation",
    "ssl_internal",
    "ssl_invalid_user_data",
    "temporary",
    "unknown_socket",
]

SOCKET_OPTION = bidict(
    low_delay=mod.SocketOption.LowDelayOption,
    keep_alive=mod.SocketOption.KeepAliveOption,
    multicast_ttl=mod.SocketOption.MulticastTtlOption,
    multicast_loopback=mod.SocketOption.MulticastLoopbackOption,
    type_of_service=mod.SocketOption.TypeOfServiceOption,
    send_buffer_size_socket=mod.SocketOption.SendBufferSizeSocketOption,
    receive_buffer_size=mod.SocketOption.ReceiveBufferSizeSocketOption,
    path_mtu_socket=mod.SocketOption.PathMtuSocketOption,
)

SocketOptionStr = Literal[
    "low_delay",
    "keep_alive",
    "multicast_ttl",
    "multicast_loopback",
    "type_of_service",
    "send_buffer_size_socket",
    "receive_buffer_size",
    "path_mtu_socket",
]

SOCKET_STATE = bidict(
    unconnected=mod.SocketState.UnconnectedState,
    host_lookup=mod.SocketState.HostLookupState,
    connecting=mod.SocketState.ConnectingState,
    connected=mod.SocketState.ConnectedState,
    bound=mod.SocketState.BoundState,
    closing=mod.SocketState.ClosingState,
    listening=mod.SocketState.ListeningState,
)

SocketStateStr = Literal[
    "unconnected",
    "host_lookup",
    "connecting",
    "connected",
    "bound",
    "closing",
    "listening",
]

SOCKET_TYPE = bidict(
    tcp=mod.SocketType.TcpSocket,
    udp=mod.SocketType.UdpSocket,
    sctp=mod.SocketType.SctpSocket,
    unknown=mod.SocketType.UnknownSocketType,
)

SocketTypeStr = Literal["tcp", "udp", "sctp", "unknown"]

TYPE_OF_SERVICE = bidict(
    network_control=224,
    internetwork_control=192,
    critic_ecp=160,
    flash_override=128,
    flash=96,
    immediate=64,
    priority=32,
    routine=0,
)

TypeOfServiceStr = Literal[
    "network_control",
    "internetwork_control",
    "critic_ecp",
    "flash_override",
    "flash",
    "immediate",
    "priority",
    "routine",
]

QtNetwork.QAbstractSocket.__bases__ = (core.IODevice,)


class AbstractSocket(QtNetwork.QAbstractSocket):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def bind_to(
        self,
        address: str | QtNetwork.QHostAddress,
        port: int = 0,
        bind_mode: (
            QtNetwork.QAbstractSocket.BindMode | BindModeStr
        ) = "default_for_platform",
    ) -> bool:
        if isinstance(address, str):
            address = QtNetwork.QHostAddress(address)
        if bind_mode in BIND_MODE:
            mode = BIND_MODE[bind_mode]
        else:
            mode = bind_mode
        return self.bind(address, port, mode)

    def connect_to_host(
        self,
        hostname: str,
        port: int,
        open_mode: (QtCore.QIODevice.OpenMode | core.iodevice.OpenModeStr) = "read_write",
        protocol: (
            QtNetwork.QAbstractSocket.NetworkLayerProtocol | NetworkLayerProtocolStr
        ) = "any_ip",
    ):
        if isinstance(open_mode, QtCore.QIODevice.OpenMode):
            mode = open_mode
        else:
            mode = core.iodevice.OPEN_MODES[open_mode]
        if isinstance(protocol, QtNetwork.QAbstractSocket.NetworkLayerProtocol):
            prot = protocol
        else:
            prot = NETWORK_LAYER_PROTOCOL[protocol]
        self.connectToHost(hostname, port, mode, prot)

    def get_error(self) -> SocketErrorStr:
        return SOCKET_ERROR.inverse[self.error()]

    def set_pause_mode(self, mode: PauseModeStr):
        """Set pause mode.

        Args:
            mode: pause mode

        Raises:
            InvalidParamError: pause mode does not exist
        """
        if mode not in PAUSE_MODES:
            raise InvalidParamError(mode, PAUSE_MODES)
        self.setPauseMode(PAUSE_MODES[mode])

    def get_pause_mode(self) -> PauseModeStr:
        return PAUSE_MODES.inverse[self.pauseMode()]

    def get_proxy(self) -> network.NetworkProxy:
        return network.NetworkProxy(self.proxy())

    # def set_socket_option(self, name: str, value):
    #     if name not in SOCKET_OPTION:
    #         raise InvalidParamError(name, SOCKET_OPTION)
    #     self.setSocketOption(SOCKET_OPTION[name], value)

    # def get_socket_option(self, name: str):
    #     return self.socketOption(SOCKET_OPTION[name])

    # def set_type_of_service(self, typ: str):
    #     if typ not in TYPE_OF_SERVICE:
    #         raise InvalidParamError(typ, TYPE_OF_SERVICE)
    #     self.set_socket_option("type_of_service", TYPE_OF_SERVICE[typ])

    # def get_type_of_service(self):
    #     opt = self.get_socket_option("type_of_service")
    #     return TYPE_OF_SERVICE.inverse[opt]

    def get_socket_type(self) -> SocketTypeStr:
        return SOCKET_TYPE.inverse[self.socketType()]

    def get_state(self) -> SocketStateStr:
        return SOCKET_STATE.inverse[self.state()]

    def get_local_address(self) -> network.HostAddress:
        return network.HostAddress(self.localAddress())
