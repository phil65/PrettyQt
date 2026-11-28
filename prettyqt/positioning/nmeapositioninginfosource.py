from typing import Literal

from prettyqt import positioning
from prettyqt.qt import QtCore, QtPositioning
from prettyqt.utils import bidict, get_repr


QNmeaPositionInfoSource = QtPositioning.QNmeaPositionInfoSource

UpdateModeStr = Literal["real_time", "simulation"]

UPDATE_MODES: bidict[UpdateModeStr, QtPositioning.QNmeaPositionInfoSource.UpdateMode] = (
    bidict(
        real_time=QtPositioning.QNmeaPositionInfoSource.UpdateMode.RealTimeMode,
        simulation=QtPositioning.QNmeaPositionInfoSource.UpdateMode.SimulationMode,
    )
)


class NmeaPositionInfoSource(
    positioning.GeoPositionInfoSourceMixin, QtPositioning.QNmeaPositionInfoSource
):
    def __init__(
        self,
        update_mode: UpdateModeStr | QtPositioning.QNmeaPositionInfoSource.UpdateMode,
        parent: QtCore.QObject | None = None,
    ):
        mode = UPDATE_MODES.get_enum_value(update_mode)
        super().__init__(mode, parent)

    def __repr__(self):
        return get_repr(self)

    def get_update_mode(self) -> UpdateModeStr:
        return UPDATE_MODES.inverse[self.updateMode()]


if __name__ == "__main__":
    obj = QtCore.QObject()
    source = NmeaPositionInfoSource("real_time", obj)
