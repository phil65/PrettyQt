"""Classes to make network programming easier and more portable."""

from __future__ import annotations

from prettyqt.qt.QtNetwork import *  # noqa: F403

from .networkcookie import NetworkCookie
from .networkcookiejar import NetworkCookieJar
from .networkreply import NetworkReply
from .networkrequest import NetworkRequest
from .networkproxy import NetworkProxy
from .hostaddress import HostAddress
from .networkaddressentry import NetworkAddressEntry
from .networkinterface import NetworkInterface
from .networkdatagram import NetworkDatagram
from .abstractsocket import AbstractSocket, AbstractSocketMixin
from .localsocket import LocalSocket
from .localserver import LocalServer
from .tcpserver import TcpServer
from .tcpsocket import TcpSocket
from .udpsocket import UdpSocket
from .httppart import HttpPart
from .httpmultipart import HttpMultiPart
from .networkaccessmanager import NetworkAccessManager
from prettyqt.qt import QtNetwork

QT_MODULE = QtNetwork

__all__ = [
    "NetworkProxy",
    "NetworkReply",
    "AbstractSocket",
    "AbstractSocketMixin",
    "LocalSocket",
    "HostAddress",
    "LocalServer",
    "TcpServer",
    "NetworkDatagram",
    "NetworkAddressEntry",
    "NetworkInterface",
    "TcpSocket",
    "UdpSocket",
    "HttpPart",
    "HttpMultiPart",
    "NetworkCookie",
    "NetworkCookieJar",
    "NetworkRequest",
    "NetworkAccessManager",
]
