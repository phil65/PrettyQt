from __future__ import annotations

from typing import Literal, Union

from prettyqt import network
from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict


CONVERSION_MODE = bidict(
    strict=QtNetwork.QHostAddress.StrictConversion,
    v4_mapped_to_ipv4=QtNetwork.QHostAddress.ConvertV4MappedToIPv4,
    v4_compat_to_ipv4=QtNetwork.QHostAddress.ConvertV4CompatToIPv4,
    localhost=QtNetwork.QHostAddress.ConvertLocalHost,
    unspecified_address=QtNetwork.QHostAddress.ConvertUnspecifiedAddress,
    tolerant=QtNetwork.QHostAddress.TolerantConversion,
)

SPECIAL_ADDRESS = bidict(
    null=int(QtNetwork.QHostAddress.Null),
    localhost=int(QtNetwork.QHostAddress.LocalHost),
    localhost_ipv6=int(QtNetwork.QHostAddress.LocalHostIPv6),
    broadcast=int(QtNetwork.QHostAddress.Broadcast),
    any_ipv4=int(QtNetwork.QHostAddress.AnyIPv4),
    any_ipv6=int(QtNetwork.QHostAddress.AnyIPv6),
    any=int(QtNetwork.QHostAddress.Any),
)

SpecialAddressStr = Literal[
    "null", "localhost", "localhost_ipv6", "broadcast", "any_ipv4", "any_ipv6", "any"
]

NetworkLayerProtocolStr = Literal["ipv4", "ipv6", "any_ip", "unknown"]


class HostAddress(QtNetwork.QHostAddress):
    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return not self.isNull()

    def get_protocol(self) -> NetworkLayerProtocolStr:
        return network.abstractsocket.NETWORK_LAYER_PROTOCOL.inverse[self.protocol()]

    def set_address(self, address: Union[int, str]):
        if address in SPECIAL_ADDRESS:
            address = SPECIAL_ADDRESS[address]
        ret = self.setAddress(address)
        if ret is False:
            raise ValueError("invalid address")
