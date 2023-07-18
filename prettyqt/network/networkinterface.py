from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.utils import bidict


INTERFACE_FLAGS = bidict(
    is_up=network.QNetworkInterface.InterfaceFlag.IsUp,
    is_running=network.QNetworkInterface.InterfaceFlag.IsRunning,
    can_broadcast=network.QNetworkInterface.InterfaceFlag.CanBroadcast,
    is_loop_back=network.QNetworkInterface.InterfaceFlag.IsLoopBack,
    is_point_to_point=network.QNetworkInterface.InterfaceFlag.IsPointToPoint,
    can_multicast=network.QNetworkInterface.InterfaceFlag.CanMulticast,
)

InterfaceFlagStr = Literal[
    "is_up",
    "is_running",
    "can_broadcast",
    "is_loop_back",
    "is_point_to_point",
    "can_multicast",
]

INTERFACE_TYPE = bidict(
    unknown=network.QNetworkInterface.InterfaceType.Unknown,
    loopback=network.QNetworkInterface.InterfaceType.Loopback,
    virtual=network.QNetworkInterface.InterfaceType.Virtual,
    ethernet=network.QNetworkInterface.InterfaceType.Ethernet,
    wifi=network.QNetworkInterface.InterfaceType.Wifi,
    can_bus=network.QNetworkInterface.InterfaceType.CanBus,
    fddi=network.QNetworkInterface.InterfaceType.Fddi,
    ppp=network.QNetworkInterface.InterfaceType.Ppp,
    slip=network.QNetworkInterface.InterfaceType.Slip,
    phonet=network.QNetworkInterface.InterfaceType.Phonet,
    ieee802154=network.QNetworkInterface.InterfaceType.Ieee802154,
    sixlowpan=network.QNetworkInterface.InterfaceType.SixLoWPAN,
    ieee80216=network.QNetworkInterface.InterfaceType.Ieee80216,
    ieee1394=network.QNetworkInterface.InterfaceType.Ieee1394,
)

InterfaceTypeStr = Literal[
    "unknown",
    "loopback",
    "virtual",
    "ethernet",
    "wifi",
    "can_bus",
    "fddi",
    "ppp",
    "slip",
    "phonet",
    "ieee802154",
    "sixlowpan",
    "ieee80216",
    "ieee1394",
]


class NetworkInterface(network.QNetworkInterface):
    """Listing of the host's IP addresses and network interfaces."""

    # def __bool__(self):
    #     return self.isValid()

    def get_type(self) -> InterfaceTypeStr:
        """Get the interface type.

        Returns:
            interface type
        """
        return INTERFACE_TYPE.inverse[self.type()]

    def get_address_entries(self) -> list[network.NetworkAddressEntry]:
        return [network.NetworkAddressEntry(i) for i in self.addressEntries()]

    @staticmethod
    def get_all_addresses() -> list[network.HostAddress]:
        return [network.HostAddress(i) for i in NetworkInterface.allAddresses()]

    @staticmethod
    def get_all_interfaces() -> list[network.HostAddress]:
        return [network.NetworkInterface(i) for i in NetworkInterface.allInterfaces()]

    @staticmethod
    def get_interface_from_name(name: str) -> NetworkInterface:
        interface = NetworkInterface.interfaceFromName(name)
        # if not interface:
        #     return None
        return NetworkInterface(interface)


if __name__ == "__main__":
    interface = NetworkInterface()
    print(bool(interface))
