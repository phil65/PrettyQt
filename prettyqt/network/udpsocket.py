from __future__ import annotations

from prettyqt import network


class UdpSocket(network.AbstractSocketMixin, network.QUdpSocket):
    """UDP Socket."""

    def get_multicast_interface(self) -> network.NetworkInterface:
        return network.NetworkInterface(self.multicastInterface())

    def receive_datagram(self, max_size: int | None = None) -> network.NetworkDatagram:
        if max_size is None:
            max_size = -1
        return network.NetworkDatagram(self.receiveDatagram(max_size))


if __name__ == "__main__":
    socket = UdpSocket()
    socket.bind_to("localhost")
    socket.get_multicast_interface()
    socket.receive_datagram()
