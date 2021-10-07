from __future__ import annotations

from prettyqt import positioning
from prettyqt.qt import QtCore, QtPositioning
from prettyqt.utils import bidict


QNmeaPositionInfoSource = QtPositioning.QNmeaPositionInfoSource

UPDATE_MODES = bidict(
    real_time=QtPositioning.QNmeaPositionInfoSource.UpdateMode.RealTimeMode,
    simulation=QtPositioning.QNmeaPositionInfoSource.UpdateMode.SimulationMode,
)

QtPositioning.QNmeaPositionInfoSource.__bases__ = (positioning.GeoPositionInfoSource,)


class NmeaPositionInfoSource(QtPositioning.QNmeaPositionInfoSource):
    def __init__(
        self,
        update_mode: QtPositioning.QNmeaPositionInfoSource.UpdateMode | str,
        parent: QtCore.QObject,
    ):
        if isinstance(update_mode, QtPositioning.QNmeaPositionInfoSource.UpdateMode):
            mode = update_mode
        else:
            mode = UPDATE_MODES[update_mode]
        super().__init__(mode, parent)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def get_update_mode(self) -> str:
        return UPDATE_MODES.inverse[self.updateMode()]


if __name__ == "__main__":
    obj = QtCore.QObject()
    source = NmeaPositionInfoSource("real_time", obj)
    print(str(source))
    print(repr(source))
