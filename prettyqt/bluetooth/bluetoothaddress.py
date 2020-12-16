from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtBluetooth
elif PYSIDE2:
    from PySide2 import QtBluetooth


class BluetoothAddress(QtBluetooth.QBluetoothAddress):
    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __bool__(self):
        return not self.isNull()


if __name__ == "__main__":
    address = BluetoothAddress()
