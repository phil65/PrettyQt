from __future__ import annotations

from prettyqt import bluetooth


class BluetoothHostInfo(bluetooth.QBluetoothHostInfo):
    def set_address(self, address: bluetooth.QBluetoothAddress | int | str):
        if isinstance(address, int | str):
            address = bluetooth.QBluetoothAddress(address)
        self.setAddress(address)

    def get_address(self) -> bluetooth.BluetoothAddress:
        return bluetooth.BluetoothAddress(self.address())


if __name__ == "__main__":
    address = BluetoothHostInfo()
