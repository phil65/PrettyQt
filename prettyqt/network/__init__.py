# -*- coding: utf-8 -*-

"""Network module.

Contains QtNetWork-based classes
"""

from .networkcookie import NetworkCookie
from .networkcookiejar import NetworkCookieJar
from .networkrequest import NetworkRequest
from .networkproxy import NetworkProxy
from .hostaddress import HostAddress
from .networkaddressentry import NetworkAddressEntry
from .networkinterface import NetworkInterface
from .networkdatagram import NetworkDatagram
from .abstractsocket import AbstractSocket
from .tcpsocket import TcpSocket
from .httppart import HttpPart
from .httpmultipart import HttpMultiPart
from .networkaccessmanager import NetworkAccessManager

__all__ = [
    "NetworkProxy",
    "AbstractSocket",
    "HostAddress",
    "NetworkDatagram",
    "NetworkAddressEntry",
    "NetworkInterface",
    "TcpSocket",
    "HttpPart",
    "HttpMultiPart",
    "NetworkCookie",
    "NetworkCookieJar",
    "NetworkRequest",
    "NetworkAccessManager",
]
