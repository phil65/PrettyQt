from qtpy import QtNetwork

from prettyqt import core, network
from prettyqt.utils import InvalidParamError, bidict, helpers


SOCKET_OPTION = bidict(
    none=QtNetwork.QLocalServer.SocketOption(0),  # QtNetwork.QLocalServer.NoOptions
    user=QtNetwork.QLocalServer.UserAccessOption,
    group=QtNetwork.QLocalServer.GroupAccessOption,
    other=QtNetwork.QLocalServer.OtherAccessOption,
    world=QtNetwork.QLocalServer.WorldAccessOption,
)

QtNetwork.QLocalServer.__bases__ = (core.Object,)


class LocalServer(QtNetwork.QLocalServer):
    def get_server_error(self) -> str:
        return network.abstractsocket.SOCKET_ERROR.inverse[self.serverError()]

    def set_socket_options(self, *name: str):
        for item in name:
            if item not in SOCKET_OPTION:
                raise InvalidParamError(item, SOCKET_OPTION)
        flags = helpers.merge_flags(name, SOCKET_OPTION)
        self.setSocketOptions(flags)

    def get_socket_options(self):
        print(self.socketOptions())
        return [k for k, v in SOCKET_OPTION.items() if v & self.socketOptions()]


if __name__ == "__main__":
    server = LocalServer()
