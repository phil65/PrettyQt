from __future__ import annotations

from prettyqt import bluetooth
from prettyqt.qt import QtBluetooth


class BluetoothHostInfo(QtBluetooth.QBluetoothHostInfo):
    def set_address(self, address: QtBluetooth.QBluetoothAddress | int | str):
        if isinstance(address, int | str):
            address = QtBluetooth.QBluetoothAddress(address)
        self.setAddress(address)

    def get_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.address())


if __name__ == "__main__":
    address = BluetoothHostInfo()
