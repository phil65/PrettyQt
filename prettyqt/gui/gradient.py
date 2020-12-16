from typing import List, Literal, Tuple

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import InvalidParamError, bidict, prettyprinter


COORDINATE_MODE = bidict(
    logical=QtGui.QGradient.LogicalMode,
    object=QtGui.QGradient.ObjectMode,
    stretch_to_device=QtGui.QGradient.StretchToDeviceMode,
    object_bounding=QtGui.QGradient.ObjectBoundingMode,
)

CoordinateModeStr = Literal["logical", "object", "stretch_to_device", "object_bounding"]

SPREAD = bidict(
    pad=QtGui.QGradient.PadSpread,
    repeat=QtGui.QGradient.RepeatSpread,
    reflect=QtGui.QGradient.ReflectSpread,
)

SpreadStr = Literal["pad", "repeat", "reflect"]

TYPE = bidict(
    linear=QtGui.QGradient.LinearGradient,
    radial=QtGui.QGradient.RadialGradient,
    conical=QtGui.QGradient.ConicalGradient,
    none=QtGui.QGradient.NoGradient,
)

TypeStr = Literal["linear", "radial", "conical", "none"]


class Gradient(prettyprinter.PrettyPrinter, QtGui.QGradient):
    def __setitem__(self, key: float, value):
        self.setColorAt(key, value)

    def serialize_fields(self):
        return dict(
            coordinate_mode=self.get_coordinate_mode(),
            spread=self.get_spread(),
            stops=self.get_stops(),
        )

    def serialize(self):
        return self.serialize_fields()

    def set_coordinate_mode(self, mode: CoordinateModeStr):
        """Set the coordinate mode.

        Args:
            mode: coordinate mode

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in COORDINATE_MODE:
            raise InvalidParamError(mode, COORDINATE_MODE)
        self.setCoordinateMode(COORDINATE_MODE[mode])

    def get_coordinate_mode(self) -> CoordinateModeStr:
        """Return current coordinate mode.

        Returns:
            coordinate mode
        """
        return COORDINATE_MODE.inverse[self.coordinateMode()]

    def set_spread(self, method: SpreadStr):
        """Set the spread method.

        Args:
            method: spread method

        Raises:
            InvalidParamError: method does not exist
        """
        if method not in SPREAD:
            raise InvalidParamError(method, SPREAD)
        self.setSpread(SPREAD[method])

    def get_spread(self) -> SpreadStr:
        """Return current spread method.

        Returns:
            spread method
        """
        return SPREAD.inverse[self.spread()]

    def get_type(self) -> TypeStr:
        """Return current gradient type.

        Returns:
            gradient type
        """
        return TYPE.inverse[self.type()]

    def get_stops(self) -> List[Tuple[float, gui.Color]]:
        return [(i, gui.Color(j)) for (i, j) in self.stops()]


if __name__ == "__main__":
    grad = Gradient()
    grad.setStops([(0.0, gui.Color("red")), (1.0, gui.Color("green"))])
    print(grad.get_stops())
    print(repr(grad))
