from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict, get_repr


HostMode = QtBluetooth.QBluetoothLocalDevice.HostMode
HOST_MODE = bidict(
    powered_off=HostMode.HostPoweredOff,
    connectable=HostMode.HostConnectable,
    discoverable=HostMode.HostDiscoverable,
    discoverable_limited_inquiry=HostMode.HostDiscoverableLimitedInquiry,
)

HostModeStr = Literal[
    "powered_off", "connectable", "discoverable", "discoverable_limited_inquiry"
]

Error = QtBluetooth.QBluetoothLocalDevice.Error

ERROR = bidict(
    none=Error.NoError,
    pairing=Error.PairingError,
    missing_permissions=Error.MissingPermissionsError,
    unknown=Error.UnknownError,
)

ErrorStr = Literal["none", "pairing", "missing_permissions", "unknown"]


Pairing = QtBluetooth.QBluetoothLocalDevice.Pairing

PAIRING = bidict(
    unpaired=Pairing.Unpaired,
    paired=Pairing.Paired,
    authorized_paired=Pairing.AuthorizedPaired,
)

PairingStr = Literal["unpaired", "paired", "authorized_paired"]


class BluetoothLocalDevice(core.ObjectMixin, QtBluetooth.QBluetoothLocalDevice):
    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.address())

    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def set_host_mode(self, mode: HostModeStr | HostMode):
        """Set host mode.

        Args:
            mode: host mode to use
        """
        self.setGridStyle(HOST_MODE.get_enum_value(mode))

    def get_host_mode(self) -> HostModeStr:
        """Return host mode.

        Returns:
            host mode
        """
        return HOST_MODE.inverse[self.gridStyle()]

    def get_pairing_status(
        self, address: QtBluetooth.QBluetoothAddress | int | str
    ) -> PairingStr:
        """Return pairing status.

        Arguments:
            address: bluetooth address

        Returns:
            pairing status
        """
        if isinstance(address, int | str):
            address = QtBluetooth.QBluetoothAddress(address)
        return PAIRING.inverse[self.pairingStatus(address)]

    def request_pairing(
        self, address: QtBluetooth.QBluetoothAddress | int | str, pairing: PairingStr
    ):
        if isinstance(address, int | str):
            address = QtBluetooth.QBluetoothAddress(address)
        self.requestPairing(address, PAIRING[pairing])

    def get_connected_devices(self) -> list[bluetooth.BluetoothAddress]:
        return [bluetooth.BluetoothAddress(i) for i in self.connectedDevices()]

    @classmethod
    def get_all_devices(cls) -> list[bluetooth.BluetoothHostInfo]:
        return [bluetooth.BluetoothHostInfo(i) for i in cls.allDevices()]


if __name__ == "__main__":
    devices = BluetoothLocalDevice.get_all_devices()
