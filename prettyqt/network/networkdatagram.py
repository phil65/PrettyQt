# -*- coding: utf-8 -*-

from qtpy import QtNetwork, QtCore

from prettyqt import network


class NetworkDatagram(QtNetwork.QNetworkDatagram):
    def get_destination_address(self) -> network.HostAddress:
        return network.HostAddress(self.destinationAddress())

    def get_sender_address(self) -> network.HostAddress:
        return network.HostAddress(self.senderAddress())

    def set_data(self, data: str):
        self.setData(QtCore.QByteArray(data.encode()))

    def get_data(self) -> str:
        return bytes(self.data()).decode()


if __name__ == "__main__":
    datagram = NetworkDatagram()
