from __future__ import annotations

from prettyqt.qt import QtBluetooth
from prettyqt.utils import get_repr


class BluetoothAddress(QtBluetooth.QBluetoothAddress):
    def __repr__(self):
        return get_repr(self, self.toString())

    def __str__(self):
        return self.toString()

    def __bool__(self):
        return not self.isNull()


if __name__ == "__main__":
    address = BluetoothAddress()
