from prettyqt import network
from prettyqt.qt import QtNetwork


QtNetwork.QTcpSocket.__bases__ = (network.AbstractSocket,)


class TcpSocket(QtNetwork.QTcpSocket):
    pass
