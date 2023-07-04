from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.utils import bidict, get_repr


HostModeStr = Literal[
    "powered_off", "connectable", "discoverable", "discoverable_limited_inquiry"
]

HostMode = bluetooth.QBluetoothLocalDevice.HostMode
HOST_MODE: bidict[HostModeStr, HostMode] = bidict(
    powered_off=HostMode.HostPoweredOff,
    connectable=HostMode.HostConnectable,
    discoverable=HostMode.HostDiscoverable,
    discoverable_limited_inquiry=HostMode.HostDiscoverableLimitedInquiry,
)


Error = bluetooth.QBluetoothLocalDevice.Error

ErrorStr = Literal["none", "pairing", "missing_permissions", "unknown"]

ERROR: bidict[ErrorStr, Error] = bidict(
    none=Error.NoError,
    pairing=Error.PairingError,
    missing_permissions=Error.MissingPermissionsError,
    unknown=Error.UnknownError,
)


Pairing = bluetooth.QBluetoothLocalDevice.Pairing

PairingStr = Literal["unpaired", "paired", "authorized_paired"]

PAIRING: bidict[PairingStr, Pairing] = bidict(
    unpaired=Pairing.Unpaired,
    paired=Pairing.Paired,
    authorized_paired=Pairing.AuthorizedPaired,
)


class BluetoothLocalDevice(core.ObjectMixin, bluetooth.QBluetoothLocalDevice):
    def __bool__(self):
        """Return True when local device is valid."""
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.address())

    def get_error(self) -> ErrorStr:
        """Get error code."""
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
        self, address: bluetooth.QBluetoothAddress | int | str
    ) -> PairingStr:
        """Return pairing status.

        Arguments:
            address: bluetooth address

        Returns:
            pairing status
        """
        if isinstance(address, int | str):
            address = bluetooth.QBluetoothAddress(address)
        return PAIRING.inverse[self.pairingStatus(address)]

    def request_pairing(
        self,
        address: bluetooth.QBluetoothAddress | int | str,
        pairing: PairingStr | Pairing,
    ):
        """Request a pairing to given bluetooth address."""
        if isinstance(address, int | str):
            address = bluetooth.QBluetoothAddress(address)
        self.requestPairing(address, PAIRING.get_enum_value(pairing))

    def get_connected_devices(self) -> list[bluetooth.BluetoothAddress]:
        """Get addresses for connected devices."""
        return [bluetooth.BluetoothAddress(i) for i in self.connectedDevices()]

    @classmethod
    def for_all_devices(cls) -> list[bluetooth.BluetoothHostInfo]:
        """Get host info for all devices."""
        return [bluetooth.BluetoothHostInfo(i) for i in cls.allDevices()]


if __name__ == "__main__":
    devices = BluetoothLocalDevice.get_all_devices()
