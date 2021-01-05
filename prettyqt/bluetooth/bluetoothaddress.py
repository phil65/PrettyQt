from __future__ import annotations

from prettyqt.qt import QtBluetooth


class BluetoothAddress(QtBluetooth.QBluetoothAddress):
    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __bool__(self):
        return not self.isNull()


if __name__ == "__main__":
    address = BluetoothAddress()
