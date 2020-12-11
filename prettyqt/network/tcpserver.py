from typing import Union

from qtpy import QtNetwork

from prettyqt import core, network


QtNetwork.QTcpServer.__bases__ = (core.Object,)


class TcpServer(QtNetwork.QTcpServer):
    def listen(self, address: Union[str, QtNetwork.QHostAddress], port: int = 0) -> bool:
        if isinstance(address, str):
            address = network.HostAddress(address)
        return super().listen(address, port)

    def get_server_address(self) -> network.HostAddress:
        return network.HostAddress(self.serverAddress())

    def get_proxy(self) -> network.NetworkProxy:
        return network.NetworkProxy(self.proxy())

    def get_server_error(self) -> str:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]
