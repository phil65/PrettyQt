from __future__ import annotations

from prettyqt import network
from prettyqt.qt import QtNetwork


class TcpSocket(network.AbstractSocketMixin, QtNetwork.QTcpSocket):
    pass
