from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.qt import QtCore
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

CAPABILITIES: bidict[CapabilityStr, network.QNetworkProxy.Capability] = bidict(
    tunneling=network.QNetworkProxy.Capability.TunnelingCapability,
    listening=network.QNetworkProxy.Capability.ListeningCapability,
    udp_tunneling=network.QNetworkProxy.Capability.UdpTunnelingCapability,
    caching=network.QNetworkProxy.Capability.CachingCapability,
    host_name_lookup=network.QNetworkProxy.Capability.HostNameLookupCapability,
    sctp_tunneling=network.QNetworkProxy.Capability.SctpTunnelingCapability,
    sctp_listening=network.QNetworkProxy.Capability.SctpListeningCapability,
)

ProxyTypeStr = Literal[
    "none",
    "default",
    "socks5",
    "http",
    "http_caching",
    "ftp_caching",
]

PROXY_TYPES: bidict[ProxyTypeStr, network.QNetworkProxy.ProxyType] = bidict(
    none=network.QNetworkProxy.ProxyType.NoProxy,
    default=network.QNetworkProxy.ProxyType.DefaultProxy,
    socks5=network.QNetworkProxy.ProxyType.Socks5Proxy,
    http=network.QNetworkProxy.ProxyType.HttpProxy,
    http_caching=network.QNetworkProxy.ProxyType.HttpCachingProxy,
    ftp_caching=network.QNetworkProxy.ProxyType.FtpCachingProxy,
)


class NetworkProxy(network.QNetworkProxy):
    """Network layer proxy."""

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

    def set_type(self, typ: ProxyTypeStr | network.QNetworkProxy.ProxyType):
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
