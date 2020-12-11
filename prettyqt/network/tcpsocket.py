from qtpy import QtNetwork

from prettyqt import network


QtNetwork.QTcpSocket.__bases__ = (network.AbstractSocket,)


class TcpSocket(QtNetwork.QTcpSocket):
    pass
