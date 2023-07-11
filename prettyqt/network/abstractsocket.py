from __future__ import annotations

from typing import Literal

from prettyqt import core, network
from prettyqt.utils import bidict, get_repr


mod = network.QAbstractSocket

BindModeStr = Literal[
    "share_address",
    "dont_share_address",
    "reuse_address_hint",
    "default_for_platform",
]

BIND_MODE: bidict[BindModeStr, mod.BindFlag] = bidict(
    share_address=mod.BindFlag.ShareAddress,
    dont_share_address=mod.BindFlag.DontShareAddress,
    reuse_address_hint=mod.BindFlag.ReuseAddressHint,
    default_for_platform=mod.BindFlag.DefaultForPlatform,
)

NetworkLayerProtocolStr = Literal["ipv4", "ipv6", "any_ip", "unknown"]

NETWORK_LAYER_PROTOCOL: bidict[NetworkLayerProtocolStr, mod.NetworkLayerProtocol] = (
    bidict(
        ipv4=mod.NetworkLayerProtocol.IPv4Protocol,
        ipv6=mod.NetworkLayerProtocol.IPv6Protocol,
        any_ip=mod.NetworkLayerProtocol.AnyIPProtocol,
        unknown=mod.NetworkLayerProtocol.UnknownNetworkLayerProtocol,
    )
)

PauseModeStr = Literal["never", "on_ssl_errors"]

PAUSE_MODES: bidict[PauseModeStr, mod.PauseMode] = bidict(
    never=mod.PauseMode.PauseNever,
    on_ssl_errors=mod.PauseMode.PauseOnSslErrors,
)

mod = mod

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

SOCKET_ERROR: bidict[SocketErrorStr, mod.SocketError] = bidict(
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

SOCKET_OPTION: bidict[SocketOptionStr, mod.SocketOption] = bidict(
    low_delay=mod.SocketOption.LowDelayOption,
    keep_alive=mod.SocketOption.KeepAliveOption,
    multicast_ttl=mod.SocketOption.MulticastTtlOption,
    multicast_loopback=mod.SocketOption.MulticastLoopbackOption,
    type_of_service=mod.SocketOption.TypeOfServiceOption,
    send_buffer_size_socket=mod.SocketOption.SendBufferSizeSocketOption,
    receive_buffer_size=mod.SocketOption.ReceiveBufferSizeSocketOption,
    path_mtu_socket=mod.SocketOption.PathMtuSocketOption,
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

SOCKET_STATE: bidict[SocketStateStr, mod.SocketState] = bidict(
    unconnected=mod.SocketState.UnconnectedState,
    host_lookup=mod.SocketState.HostLookupState,
    connecting=mod.SocketState.ConnectingState,
    connected=mod.SocketState.ConnectedState,
    bound=mod.SocketState.BoundState,
    closing=mod.SocketState.ClosingState,
    listening=mod.SocketState.ListeningState,
)

SocketTypeStr = Literal["tcp", "udp", "sctp", "unknown"]

SOCKET_TYPE: bidict[SocketTypeStr, mod.SocketType] = bidict(
    tcp=mod.SocketType.TcpSocket,
    udp=mod.SocketType.UdpSocket,
    sctp=mod.SocketType.SctpSocket,
    unknown=mod.SocketType.UnknownSocketType,
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

TYPE_OF_SERVICE: bidict[TypeOfServiceStr, int] = bidict(
    network_control=224,
    internetwork_control=192,
    critic_ecp=160,
    flash_override=128,
    flash=96,
    immediate=64,
    priority=32,
    routine=0,
)


class AbstractSocketMixin(core.IODeviceMixin):
    def __repr__(self):
        return get_repr(self)

    def bind_to(
        self,
        address: str | network.QHostAddress,
        port: int = 0,
        bind_mode: (
            network.QAbstractSocket.BindFlag | BindModeStr
        ) = "default_for_platform",
    ) -> bool:
        if isinstance(address, str):
            address = network.QHostAddress(address)
        mode = BIND_MODE.get_enum_value(bind_mode)
        return self.bind(address, port, mode)

    def connect_to_host(
        self,
        hostname: str,
        port: int,
        open_mode: core.QIODevice.OpenModeFlag | core.iodevice.OpenModeStr = "read_write",
        protocol: (
            network.QAbstractSocket.NetworkLayerProtocol | NetworkLayerProtocolStr
        ) = "any_ip",
    ):
        mode = core.iodevice.OPEN_MODES.get_enum_value(open_mode)
        prot = NETWORK_LAYER_PROTOCOL.get_enum_value(protocol)
        self.connectToHost(hostname, port, mode, prot)

    def get_error(self) -> SocketErrorStr:
        return SOCKET_ERROR.inverse[self.error()]

    def set_pause_mode(self, mode: PauseModeStr | mod.PauseMode):
        """Set pause mode.

        Args:
            mode: pause mode
        """
        self.setPauseMode(PAUSE_MODES.get_enum_value(mode))

    def get_pause_mode(self) -> PauseModeStr:
        return PAUSE_MODES.inverse[self.pauseMode()]

    def get_proxy(self) -> network.NetworkProxy:
        return network.NetworkProxy(self.proxy())

    # def set_socket_option(self, name: str, value):
    #     self.setSocketOption(SOCKET_OPTION.get_enum_value(name), value)

    # def get_socket_option(self, name: str):
    #     return self.socketOption(SOCKET_OPTION.get_enum_value(name))

    # def set_type_of_service(self, typ: str):
    #     self.set_socket_option("type_of_service", TYPE_OF_SERVICE.get_enum_value(typ))

    # def get_type_of_service(self):
    #     opt = self.get_socket_option("type_of_service")
    #     return TYPE_OF_SERVICE.inverse[opt]

    def get_socket_type(self) -> SocketTypeStr:
        return SOCKET_TYPE.inverse[self.socketType()]

    def get_state(self) -> SocketStateStr:
        return SOCKET_STATE.inverse[self.state()]

    def get_local_address(self) -> network.HostAddress:
        return network.HostAddress(self.localAddress())


class AbstractSocket(AbstractSocketMixin, network.QAbstractSocket):
    pass
