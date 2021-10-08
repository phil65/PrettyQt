from __future__ import annotations

from typing import Literal

from prettyqt import network
from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict


INTERFACE_FLAGS = bidict(
    is_up=QtNetwork.QNetworkInterface.InterfaceFlag.IsUp,
    is_running=QtNetwork.QNetworkInterface.InterfaceFlag.IsRunning,
    can_broadcast=QtNetwork.QNetworkInterface.InterfaceFlag.CanBroadcast,
    is_loop_back=QtNetwork.QNetworkInterface.InterfaceFlag.IsLoopBack,
    is_point_to_point=QtNetwork.QNetworkInterface.InterfaceFlag.IsPointToPoint,
    can_multicast=QtNetwork.QNetworkInterface.InterfaceFlag.CanMulticast,
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
    unknown=QtNetwork.QNetworkInterface.InterfaceType.Unknown,
    loopback=QtNetwork.QNetworkInterface.InterfaceType.Loopback,
    virtual=QtNetwork.QNetworkInterface.InterfaceType.Virtual,
    ethernet=QtNetwork.QNetworkInterface.InterfaceType.Ethernet,
    wifi=QtNetwork.QNetworkInterface.InterfaceType.Wifi,
    can_bus=QtNetwork.QNetworkInterface.InterfaceType.CanBus,
    fddi=QtNetwork.QNetworkInterface.InterfaceType.Fddi,
    ppp=QtNetwork.QNetworkInterface.InterfaceType.Ppp,
    slip=QtNetwork.QNetworkInterface.InterfaceType.Slip,
    phonet=QtNetwork.QNetworkInterface.InterfaceType.Phonet,
    ieee802154=QtNetwork.QNetworkInterface.InterfaceType.Ieee802154,
    sixlowpan=QtNetwork.QNetworkInterface.InterfaceType.SixLoWPAN,
    ieee80216=QtNetwork.QNetworkInterface.InterfaceType.Ieee80216,
    ieee1394=QtNetwork.QNetworkInterface.InterfaceType.Ieee1394,
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


class NetworkInterface(QtNetwork.QNetworkInterface):
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
