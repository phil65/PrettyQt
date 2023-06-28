from __future__ import annotations

from prettyqt import core, network


class TcpServer(core.ObjectMixin, network.QTcpServer):
    def listen(  # type: ignore
        self, address: str | network.QHostAddress, port: int = 0
    ) -> bool:
        if isinstance(address, str):
            address = network.HostAddress(address)
        return super().listen(address, port)

    def get_server_address(self) -> network.HostAddress:
        return network.HostAddress(self.serverAddress())

    def get_proxy(self) -> network.NetworkProxy:
        return network.NetworkProxy(self.proxy())

    def get_server_error(self) -> network.abstractsocket.SocketErrorStr:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]
