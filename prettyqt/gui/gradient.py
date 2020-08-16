# -*- coding: utf-8 -*-

from typing import Tuple, List

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError, prettyprinter


COORDINATE_MODES = bidict(
    logical=QtGui.QGradient.LogicalMode,
    object=QtGui.QGradient.ObjectMode,
    stretch_to_device=QtGui.QGradient.StretchToDeviceMode,
    object_bounding=QtGui.QGradient.ObjectBoundingMode,
)

SPREADS = bidict(
    pad=QtGui.QGradient.PadSpread,
    repeat=QtGui.QGradient.RepeatSpread,
    reflect=QtGui.QGradient.ReflectSpread,
)


TYPES = bidict(
    linear=QtGui.QGradient.LinearGradient,
    radial=QtGui.QGradient.RadialGradient,
    conical=QtGui.QGradient.ConicalGradient,
    none=QtGui.QGradient.NoGradient,
)


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

    def set_coordinate_mode(self, mode: str):
        """Set the coordinate mode.

        Allowed values are "logical", "object", "stretch_to_device", "object_bounding"

        Args:
            mode: coordinate mode

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in COORDINATE_MODES:
            raise InvalidParamError(mode, COORDINATE_MODES)
        self.setCoordinateMode(COORDINATE_MODES[mode])

    def get_coordinate_mode(self) -> str:
        """Return current coordinate mode.

        Possible values: "logical", "object", "stretch_to_device", "object_bounding"

        Returns:
            coordinate mode
        """
        return COORDINATE_MODES.inv[self.coordinateMode()]

    def set_spread(self, method: str):
        """Set the spread method.

        Allowed values are "pad", "repeat", "reflect"

        Args:
            method: spread method

        Raises:
            InvalidParamError: method does not exist
        """
        if method not in SPREADS:
            raise InvalidParamError(method, SPREADS)
        self.setSpread(SPREADS[method])

    def get_spread(self) -> str:
        """Return current spread method.

        Possible values: "pad", "repeat", "reflect"

        Returns:
            spread method
        """
        return SPREADS.inv[self.spread()]

    def get_type(self) -> str:
        """Return current gradient type.

        Possible values: "linear", "radial", "conical", "none"

        Returns:
            gradient type
        """
        return TYPES.inv[self.type()]

    def get_stops(self) -> List[Tuple[float, gui.Color]]:
        return [(i, gui.Color(j)) for (i, j) in self.stops()]


if __name__ == "__main__":
    grad = Gradient()
    grad.setStops([(0.0, gui.Color("red")), (1.0, gui.Color("green"))])
    print(grad.get_stops())
    print(repr(grad))
