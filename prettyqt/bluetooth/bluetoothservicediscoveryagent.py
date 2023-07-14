from __future__ import annotations

from typing import Literal

from prettyqt import bluetooth, core
from prettyqt.utils import bidict


module = bluetooth.QBluetoothServiceDiscoveryAgent

DiscoveryModeStr = Literal["minimal", "full"]

DISCOVERY_MODES: bidict[DiscoveryModeStr, module.DiscoveryMode] = bidict(
    minimal=module.DiscoveryMode.MinimalDiscovery,
    full=module.DiscoveryMode.FullDiscovery,
)

ErrorStr = Literal[
    "none", "powered_off", "input_output", "invalid_bluetooth_adapter", "unknown"
]

ERRORS: bidict[ErrorStr, module.Error] = bidict(
    none=module.Error.NoError,
    powered_off=module.Error.PoweredOffError,
    input_output=module.Error.InputOutputError,
    invalid_bluetooth_adapter=module.Error.InvalidBluetoothAdapterError,
    unknown=module.Error.UnknownError,
)


class BluetoothServiceDiscoveryAgent(
    core.ObjectMixin, bluetooth.QBluetoothServiceDiscoveryAgent
):
    """Enables you to query for Bluetooth services."""

    def start_discovery(self, full: bool = False):
        """Start bluetooth service discovery.

        Arguments:
            full: full discovery instead of minimal discovery.
        """
        if full:
            flag = bluetooth.QBluetoothServiceDiscoveryAgent.FullDiscovery
        else:
            flag = bluetooth.QBluetoothServiceDiscoveryAgent.MinimalDiscovery
        self.start(flag)

    def get_error(self) -> ErrorStr:
        """Get error code."""
        return ERRORS.inverse[self.error()]

    def set_remote_address(
        self, address: str | int | bluetooth.QBluetoothAddress
    ) -> bool:
        """Set remote address.

        Arguments:
            address: address of the remote
        """
        address = bluetooth.BluetoothAddress(address)
        return self.setRemoteAddress(address)

    def get_discovered_services(self) -> list[bluetooth.BluetoothServiceInfo]:
        """Get list of discovered devices."""
        return [bluetooth.BluetoothServiceInfo(i) for i in self.discoveredServices()]
