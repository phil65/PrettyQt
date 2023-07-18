from __future__ import annotations

from prettyqt import network
from prettyqt.qt import QtCore


class NetworkDatagram(network.QNetworkDatagram):
    """The data and metadata of a UDP datagram."""

    def get_destination_address(self) -> network.HostAddress:
        return network.HostAddress(self.destinationAddress())

    def get_sender_address(self) -> network.HostAddress:
        return network.HostAddress(self.senderAddress())

    def set_data(self, data: str):
        self.setData(QtCore.QByteArray(data.encode()))

    def get_data(self) -> str:
        return self.data().data().decode()


if __name__ == "__main__":
    datagram = NetworkDatagram()
