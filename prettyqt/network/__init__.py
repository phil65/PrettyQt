"""Classes to make network programming easier and more portable."""

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
from .httpheaders import HttpHeaders
from .networkrequestfactory import NetworkRequestFactory
from .networkaccessmanager import NetworkAccessManager
from .restreply import RestReply
from .restaccessmanager import RestAccessManager
from prettyqt.qt import QtNetwork

QT_MODULE = QtNetwork

__all__ = [
    "AbstractSocket",
    "AbstractSocketMixin",
    "HostAddress",
    "HttpHeaders",
    "HttpMultiPart",
    "HttpPart",
    "LocalServer",
    "LocalSocket",
    "NetworkAccessManager",
    "NetworkAddressEntry",
    "NetworkCookie",
    "NetworkCookieJar",
    "NetworkDatagram",
    "NetworkInterface",
    "NetworkProxy",
    "NetworkReply",
    "NetworkRequest",
    "NetworkRequestFactory",
    "RestAccessManager",
    "RestReply",
    "TcpServer",
    "TcpSocket",
    "UdpSocket",
]
