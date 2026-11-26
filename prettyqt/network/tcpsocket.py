from prettyqt import network


class TcpSocket(network.AbstractSocketMixin, network.QTcpSocket):
    """TCP Socket."""
