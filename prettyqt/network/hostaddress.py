from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, mappers


mod = QtNetwork.QHostAddress

CONVERSION_MODE = bidict(
    strict=mod.ConversionModeFlag.StrictConversion,
    v4_mapped_to_ipv4=mod.ConversionModeFlag.ConvertV4MappedToIPv4,
    v4_compat_to_ipv4=mod.ConversionModeFlag.ConvertV4CompatToIPv4,
    localhost=mod.ConversionModeFlag.ConvertLocalHost,
    unspecified_address=mod.ConversionModeFlag.ConvertUnspecifiedAddress,
    tolerant=mod.ConversionModeFlag.TolerantConversion,
)

SPECIAL_ADDRESS = mappers.FlagMap(
    mod.SpecialAddress,
    null=mod.SpecialAddress.Null,
    localhost=mod.SpecialAddress.LocalHost,
    localhost_ipv6=mod.SpecialAddress.LocalHostIPv6,
    broadcast=mod.SpecialAddress.Broadcast,
    any_ipv4=mod.SpecialAddress.AnyIPv4,
    any_ipv6=mod.SpecialAddress.AnyIPv6,
    any=mod.SpecialAddress.Any,
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

    def set_address(self, address: int | str):
        if address in SPECIAL_ADDRESS:
            address = SPECIAL_ADDRESS[address]
        ret = self.setAddress(address)
        if ret is False:
            raise ValueError("invalid address")
