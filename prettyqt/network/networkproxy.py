from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import bidict


CapabilityStr = Literal[
    "tunneling",
    "listening",
    "udp_tunneling",
    "caching",
    "host_name_lookup",
    "sctp_tunneling",
    "sctp_listening",
]

CAPABILITIES: bidict[CapabilityStr, QtNetwork.QNetworkProxy.Capability] = bidict(
    tunneling=QtNetwork.QNetworkProxy.Capability.TunnelingCapability,
    listening=QtNetwork.QNetworkProxy.Capability.ListeningCapability,
    udp_tunneling=QtNetwork.QNetworkProxy.Capability.UdpTunnelingCapability,
    caching=QtNetwork.QNetworkProxy.Capability.CachingCapability,
    host_name_lookup=QtNetwork.QNetworkProxy.Capability.HostNameLookupCapability,
    sctp_tunneling=QtNetwork.QNetworkProxy.Capability.SctpTunnelingCapability,
    sctp_listening=QtNetwork.QNetworkProxy.Capability.SctpListeningCapability,
)

ProxyTypeStr = Literal[
    "none",
    "default",
    "socks5",
    "http",
    "http_caching",
    "ftp_caching",
]

PROXY_TYPES: bidict[ProxyTypeStr, QtNetwork.QNetworkProxy.ProxyType] = bidict(
    none=QtNetwork.QNetworkProxy.ProxyType.NoProxy,
    default=QtNetwork.QNetworkProxy.ProxyType.DefaultProxy,
    socks5=QtNetwork.QNetworkProxy.ProxyType.Socks5Proxy,
    http=QtNetwork.QNetworkProxy.ProxyType.HttpProxy,
    http_caching=QtNetwork.QNetworkProxy.ProxyType.HttpCachingProxy,
    ftp_caching=QtNetwork.QNetworkProxy.ProxyType.FtpCachingProxy,
)


class NetworkProxy(QtNetwork.QNetworkProxy):
    def get_capabilities(self) -> list[CapabilityStr]:
        return CAPABILITIES.get_list(self.capabilities())

    def set_capabilities(self, *capability: CapabilityStr):
        flags = CAPABILITIES.merge_flags(capability)
        self.setCapabilities(flags)

    def get_header(
        self,
        name: network.networkrequest.KnownHeaderStr | network.NetworkRequest.KnownHeaders,
    ) -> str:
        return self.header(network.networkrequest.KNOWN_HEADER.get_enum_value(name))

    def set_header(
        self,
        name: network.networkrequest.KnownHeaderStr | network.NetworkRequest.KnownHeaders,
        value: str,
    ):
        self.setHeader(network.networkrequest.KNOWN_HEADER.get_enum_value(name), value)

    def get_headers(self) -> dict[str, str]:
        return {
            h.data().decode(): self.rawHeader(h).data().decode()
            for h in self.rawHeaderList()
        }

    def set_headers(self, headers: dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(
                QtCore.QByteArray(k.encode()), QtCore.QByteArray(v.encode())
            )

    def set_type(self, typ: ProxyTypeStr | QtNetwork.QNetworkProxy.ProxyType):
        """Set proxy type.

        Args:
            typ: proxy type
        """
        self.setType(PROXY_TYPES.get_enum_value(typ))

    def get_type(self) -> ProxyTypeStr:
        """Get the proxy type.

        Returns:
            type
        """
        return PROXY_TYPES.inverse[self.type()]
