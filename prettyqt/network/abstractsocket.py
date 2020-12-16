from typing import Union

from qtpy import QtNetwork

from prettyqt import core, network
from prettyqt.utils import InvalidParamError, bidict, mappers


BIND_MODE = bidict(
    share_address=QtNetwork.QAbstractSocket.ShareAddress,
    dont_share_address=QtNetwork.QAbstractSocket.DontShareAddress,
    reuse_address_hint=QtNetwork.QAbstractSocket.ReuseAddressHint,
    default_for_platform=QtNetwork.QAbstractSocket.DefaultForPlatform,
)

NETWORK_LAYER_PROTOCOL = bidict(
    ipv4=QtNetwork.QAbstractSocket.IPv4Protocol,
    ipv6=QtNetwork.QAbstractSocket.IPv6Protocol,
    any_ip=QtNetwork.QAbstractSocket.AnyIPProtocol,
    unknown=QtNetwork.QAbstractSocket.UnknownNetworkLayerProtocol,
)

PAUSE_MODES = mappers.FlagMap(
    QtNetwork.QAbstractSocket.PauseModes,
    never=QtNetwork.QAbstractSocket.PauseNever,
    on_ssl_errors=QtNetwork.QAbstractSocket.PauseOnSslErrors,
)

QAbstractSocket = QtNetwork.QAbstractSocket

SOCKET_ERROR = bidict(
    connection_refused=QAbstractSocket.ConnectionRefusedError,
    remote_host_closed=QAbstractSocket.RemoteHostClosedError,
    host_not_found=QAbstractSocket.HostNotFoundError,
    socket_access=QAbstractSocket.SocketAccessError,
    socket_resource=QAbstractSocket.SocketResourceError,
    socket_timeout=QAbstractSocket.SocketTimeoutError,
    diagram_too_large=QAbstractSocket.DatagramTooLargeError,
    network=QAbstractSocket.NetworkError,
    address_in_use=QAbstractSocket.AddressInUseError,
    socket_address_not_available=QAbstractSocket.SocketAddressNotAvailableError,
    unsupported_socket_operation=QAbstractSocket.UnsupportedSocketOperationError,
    proxy_authentication_required=QAbstractSocket.ProxyAuthenticationRequiredError,
    ssl_handshake_failed=QAbstractSocket.SslHandshakeFailedError,
    unfinished_socket_operation=QAbstractSocket.UnfinishedSocketOperationError,
    proxy_connection_refused=QAbstractSocket.ProxyConnectionRefusedError,
    proxy_connection_closed=QAbstractSocket.ProxyConnectionClosedError,
    proxy_connection_timeout=QAbstractSocket.ProxyConnectionTimeoutError,
    proxy_not_found=QAbstractSocket.ProxyNotFoundError,
    proxy_protocol=QAbstractSocket.ProxyProtocolError,
    operation=QAbstractSocket.OperationError,
    ssl_internal=QAbstractSocket.SslInternalError,
    ssl_invalid_user_data=QAbstractSocket.SslInvalidUserDataError,
    temporary=QAbstractSocket.TemporaryError,
    unknown_socket=QAbstractSocket.UnknownSocketError,
)

SOCKET_OPTION = bidict(
    low_delay=QtNetwork.QAbstractSocket.LowDelayOption,
    keep_alive=QtNetwork.QAbstractSocket.KeepAliveOption,
    multicast_ttl=QtNetwork.QAbstractSocket.MulticastTtlOption,
    multicast_loopback=QtNetwork.QAbstractSocket.MulticastLoopbackOption,
    type_of_service=QtNetwork.QAbstractSocket.TypeOfServiceOption,
    send_buffer_size_socket=QtNetwork.QAbstractSocket.SendBufferSizeSocketOption,
    receive_buffer_size=QtNetwork.QAbstractSocket.ReceiveBufferSizeSocketOption,
    path_mtu_socket=QtNetwork.QAbstractSocket.PathMtuSocketOption,
)


SOCKET_STATE = bidict(
    unconnected=QtNetwork.QAbstractSocket.UnconnectedState,
    host_lookup=QtNetwork.QAbstractSocket.HostLookupState,
    connecting=QtNetwork.QAbstractSocket.ConnectingState,
    connected=QtNetwork.QAbstractSocket.ConnectedState,
    bound=QtNetwork.QAbstractSocket.BoundState,
    closing=QtNetwork.QAbstractSocket.ClosingState,
    listening=QtNetwork.QAbstractSocket.ListeningState,
)

SOCKET_TYPE = bidict(
    tcp=QtNetwork.QAbstractSocket.TcpSocket,
    udp=QtNetwork.QAbstractSocket.UdpSocket,
    sctp=QtNetwork.QAbstractSocket.SctpSocket,
    unknown=QtNetwork.QAbstractSocket.UnknownSocketType,
)

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

QtNetwork.QAbstractSocket.__bases__ = (core.IODevice,)


class AbstractSocket(QtNetwork.QAbstractSocket):
    def __repr__(self):
        return f"{type(self).__name__}()"

    def bind(
        self,
        address: Union[str, QtNetwork.QHostAddress],
        port: int = 0,
        bind_mode: Union[int, str] = "default_for_platform",
    ):
        if isinstance(address, str):
            address = QtNetwork.QHostAddress(address)
        if bind_mode in BIND_MODE:
            bind_mode = BIND_MODE[bind_mode]
        super().bind(address, port, bind_mode)

    def connect_to_host(
        self,
        hostname: str,
        port: int,
        open_mode: Union[int, str] = "read_write",
        protocol: Union[int, str] = "any_ip",
    ):
        if open_mode in core.iodevice.OPEN_MODES:
            open_mode = core.iodevice.OPEN_MODES[open_mode]
        if protocol in NETWORK_LAYER_PROTOCOL:
            protocol = NETWORK_LAYER_PROTOCOL[protocol]
        super().connectToHost(hostname, port, open_mode, protocol)

    def get_error(self) -> str:
        return SOCKET_ERROR.inverse[self.error()]

    def set_pause_mode(self, mode: str):
        """Set pause mode.

        Valid values: "never", "on_ssl_errors"

        Args:
            mode: pause mode

        Raises:
            InvalidParamError: pause mode does not exist
        """
        if mode not in PAUSE_MODES:
            raise InvalidParamError(mode, PAUSE_MODES)
        self.setPauseMode(PAUSE_MODES[mode])

    def get_pause_mode(self) -> str:
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

    def get_socket_type(self) -> str:
        return SOCKET_TYPE.inverse[self.socketType()]

    def get_state(self) -> str:
        return SOCKET_STATE.inverse[self.state()]

    def get_local_address(self) -> network.HostAddress:
        return network.HostAddress(self.localAddress())
