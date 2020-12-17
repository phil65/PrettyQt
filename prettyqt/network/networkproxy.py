from typing import Dict, List, Literal

from qtpy import QtNetwork

from prettyqt import network
from prettyqt.utils import InvalidParamError, bidict, helpers


CAPABILITIES = bidict(
    tunneling=QtNetwork.QNetworkProxy.TunnelingCapability,
    listening=QtNetwork.QNetworkProxy.ListeningCapability,
    udp_tunneling=QtNetwork.QNetworkProxy.UdpTunnelingCapability,
    caching=QtNetwork.QNetworkProxy.CachingCapability,
    host_name_lookup=QtNetwork.QNetworkProxy.HostNameLookupCapability,
    sctp_tunneling=QtNetwork.QNetworkProxy.SctpTunnelingCapability,
    sctp_listening=QtNetwork.QNetworkProxy.SctpListeningCapability,
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
    none=QtNetwork.QNetworkProxy.NoProxy,
    default=QtNetwork.QNetworkProxy.DefaultProxy,
    socks5=QtNetwork.QNetworkProxy.Socks5Proxy,
    http=QtNetwork.QNetworkProxy.HttpProxy,
    http_caching=QtNetwork.QNetworkProxy.HttpCachingProxy,
    ftp_caching=QtNetwork.QNetworkProxy.FtpCachingProxy,
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
    def get_capabilities(self) -> List[CapabilityStr]:
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

    def get_headers(self) -> Dict[str, str]:
        return {
            bytes(h).decode(): bytes(self.rawHeader(h)).decode()
            for h in self.rawHeaderList()
        }

    def set_headers(self, headers: Dict[str, str]):
        for k, v in headers.items():
            self.setRawHeader(k.encode(), v.encode())

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
