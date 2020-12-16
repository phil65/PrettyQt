from typing import Union

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtPositioning
elif PYSIDE2:
    from PySide2 import QtPositioning

from qtpy import QtCore

from prettyqt import positioning
from prettyqt.utils import bidict


QNmeaPositionInfoSource = QtPositioning.QNmeaPositionInfoSource

UPDATE_MODES = bidict(
    real_time=QtPositioning.QNmeaPositionInfoSource.RealTimeMode,
    simulation=QtPositioning.QNmeaPositionInfoSource.SimulationMode,
)

QtPositioning.QNmeaPositionInfoSource.__bases__ = (positioning.GeoPositionInfoSource,)


class NmeaPositionInfoSource(QtPositioning.QNmeaPositionInfoSource):
    def __init__(self, update_mode: Union[int, str], parent: QtCore.QObject):
        if update_mode in UPDATE_MODES:
            update_mode = UPDATE_MODES[update_mode]
        super().__init__(update_mode, parent)

    def __repr__(self):
        return "NmeaPositionInfoSource()"

    def get_update_mode(self) -> str:
        return UPDATE_MODES.inverse[self.updateMode()]


if __name__ == "__main__":
    obj = QtCore.QObject()
    source = NmeaPositionInfoSource("real_time", obj)
    print(str(source))
    print(repr(source))
