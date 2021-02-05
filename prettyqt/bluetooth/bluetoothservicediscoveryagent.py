from __future__ import annotations

from prettyqt import bluetooth, core
from prettyqt.qt import QtBluetooth
from prettyqt.utils import bidict


DISCOVERY_MODES = bidict(
    minimal=QtBluetooth.QBluetoothServiceDiscoveryAgent.MinimalDiscovery,
    full=QtBluetooth.QBluetoothServiceDiscoveryAgent.FullDiscovery,
)

module = QtBluetooth.QBluetoothServiceDiscoveryAgent

ERRORS = bidict(
    none=module.NoError,
    powered_off=module.PoweredOffError,
    input_output=module.InputOutputError,
    invalid_bluetooth_adapter=module.InvalidBluetoothAdapterError,
    unknown=module.UnknownError,
)


QtBluetooth.QBluetoothServiceDiscoveryAgent.__bases__ = (core.Object,)


class BluetoothServiceDiscoveryAgent(QtBluetooth.QBluetoothServiceDiscoveryAgent):
    def start_discovery(self, full: bool = False):
        if full:
            flag = QtBluetooth.QBluetoothServiceDiscoveryAgent.FullDiscovery
        else:
            flag = QtBluetooth.QBluetoothServiceDiscoveryAgent.MinimalDiscovery
        self.start(flag)

    def get_error(self) -> str:
        return ERRORS.inverse[self.error()]

    def set_remote_address(
        self, address: str | int | QtBluetooth.QBluetoothAddress
    ) -> bool:
        address = bluetooth.BluetoothAddress(address)
        return self.setRemoteAddress(address)

    def get_discovered_services(self) -> list[bluetooth.BluetoothServiceInfo]:
        return [bluetooth.BluetoothServiceInfo(i) for i in self.discoveredServices()]
