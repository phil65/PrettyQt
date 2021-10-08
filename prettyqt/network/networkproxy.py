from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import InvalidParamError, bidict, helpers


CAPABILITIES = bidict(
    tunneling=QtNetwork.QNetworkProxy.Capability.TunnelingCapability,
    listening=QtNetwork.QNetworkProxy.Capability.ListeningCapability,
    udp_tunneling=QtNetwork.QNetworkProxy.Capability.UdpTunnelingCapability,
    caching=QtNetwork.QNetworkProxy.Capability.CachingCapability,
    host_name_lookup=QtNetwork.QNetworkProxy.Capability.HostNameLookupCapability,
    sctp_tunneling=QtNetwork.QNetworkProxy.Capability.SctpTunnelingCapability,
    sctp_listening=QtNetwork.QNetworkProxy.Capability.SctpListeningCapability,
)

CapabilityStr = Literal[
    "tunneling",
    "listening",
    "udp_tunneling",
    "caching",
    "host_name_lookup",
    "sctp_tunneling",
    "sctp_listening",
]

PROXY_TYPES = bidict(
    none=QtNetwork.QNetworkProxy.ProxyType.NoProxy,
    default=QtNetwork.QNetworkProxy.ProxyType.DefaultProxy,
    socks5=QtNetwork.QNetworkProxy.ProxyType.Socks5Proxy,
    http=QtNetwork.QNetworkProxy.ProxyType.HttpProxy,
    http_caching=QtNetwork.QNetworkProxy.ProxyType.HttpCachingProxy,
    ftp_caching=QtNetwork.QNetworkProxy.ProxyType.FtpCachingProxy,
)

ProxyTypeStr = Literal[
    "none",
    "default",
    "socks5",
    "http",
    "http_caching",
    "ftp_caching",
]


class NetworkProxy(QtNetwork.QNetworkProxy):
    def get_capabilities(self) -> list[CapabilityStr]:
        return [k for k, v in CAPABILITIES.items() if v & self.capabilities()]

    def set_capabilities(self, *capability: CapabilityStr):
        for item in capability:
            if item not in CAPABILITIES:
                raise InvalidParamError(item, CAPABILITIES)
        flags = helpers.merge_flags(capability, CAPABILITIES)
        self.setCapabilities(flags)

    def get_header(self, name: network.networkrequest.KnownHeaderStr) -> str:
        if name not in network.networkrequest.KNOWN_HEADER:
            raise InvalidParamError(name, network.networkrequest.KNOWN_HEADER)
        return self.header(network.networkrequest.KNOWN_HEADER[name])

    def set_header(self, name: network.networkrequest.KnownHeaderStr, value: str):
        if name not in network.networkrequest.KNOWN_HEADER:
            raise InvalidParamError(name, network.networkrequest.KNOWN_HEADER)
        self.setHeader(network.networkrequest.KNOWN_HEADER[name], value)

    def get_headers(self) -> dict[str, str]:
        return {
            bytes(h).decode(): bytes(self.rawHeader(h)).decode()
            for h in self.rawHeaderList()
        }

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def set_type(self, typ: ProxyTypeStr):
        """Set proxy type.

        Args:
            typ: proxy type

        Raises:
            InvalidParamError: proxy type does not exist
        """
        if typ not in PROXY_TYPES:
            raise InvalidParamError(typ, PROXY_TYPES)
        self.setType(PROXY_TYPES[typ])

    def get_type(self) -> ProxyTypeStr:
        """Get the proxy type.

        Returns:
            type
        """
        return PROXY_TYPES.inverse[self.type()]
