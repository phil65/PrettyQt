from __future__ import annotations

from typing import List

from qtpy import QtNetwork

from prettyqt import network
from prettyqt.utils import bidict


INTERFACE_FLAGS = bidict(
    is_up=QtNetwork.QNetworkInterface.IsUp,
    is_running=QtNetwork.QNetworkInterface.IsRunning,
    can_broadcast=QtNetwork.QNetworkInterface.CanBroadcast,
    is_loop_back=QtNetwork.QNetworkInterface.IsLoopBack,
    is_point_to_point=QtNetwork.QNetworkInterface.IsPointToPoint,
    can_multicast=QtNetwork.QNetworkInterface.CanMulticast,
)

INTERFACE_TYPES = bidict(
    unknown=QtNetwork.QNetworkInterface.Unknown,
    loopback=QtNetwork.QNetworkInterface.Loopback,
    virtual=QtNetwork.QNetworkInterface.Virtual,
    ethernet=QtNetwork.QNetworkInterface.Ethernet,
    wifi=QtNetwork.QNetworkInterface.Wifi,
    can_bus=QtNetwork.QNetworkInterface.CanBus,
    fddi=QtNetwork.QNetworkInterface.Fddi,
    ppp=QtNetwork.QNetworkInterface.Ppp,
    slip=QtNetwork.QNetworkInterface.Slip,
    phonet=QtNetwork.QNetworkInterface.Phonet,
    ieee802154=QtNetwork.QNetworkInterface.Ieee802154,
    sixlowpan=QtNetwork.QNetworkInterface.SixLoWPAN,
    ieee80216=QtNetwork.QNetworkInterface.Ieee80216,
    ieee1394=QtNetwork.QNetworkInterface.Ieee1394,
)


class NetworkInterface(QtNetwork.QNetworkInterface):
    # def __bool__(self):
    #     return self.isValid()

    def get_type(self) -> str:
        """Get the interface type.

        Possible values: "unknown", "loopback", "virtual", "ethernet", "wifi",
                         "can_bus", "fddi", "ppp", "slip", "phonet"
                         "ieee802154", "sixlowpan", "ieee80216", "ieee1394"

        Returns:
            interface type
        """
        return INTERFACE_TYPES.inverse[self.type()]

    def get_address_entries(self) -> List[network.NetworkAddressEntry]:
        return [network.NetworkAddressEntry(i) for i in self.addressEntries()]

    @staticmethod
    def get_all_addresses() -> List[network.HostAddress]:
        return [network.HostAddress(i) for i in NetworkInterface.allAddresses()]

    @staticmethod
    def get_all_interfaces() -> List[network.HostAddress]:
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
