from typing import Literal

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    standard=QtGui.QPageLayout.StandardMode, full_page=QtGui.QPageLayout.FullPageMode
)

ModeStr = Literal["standard", "full_page"]

ORIENTATIONS = bidict(
    portrait=QtGui.QPageLayout.Portrait, landscape=QtGui.QPageLayout.Landscape
)

OrientationStr = Literal["portrait", "landscape"]

UNITS = bidict(
    millimeter=QtGui.QPageLayout.Millimeter,
    point=QtGui.QPageLayout.Point,
    inch=QtGui.QPageLayout.Inch,
    pica=QtGui.QPageLayout.Pica,
    didot=QtGui.QPageLayout.Didot,
    cicero=QtGui.QPageLayout.Cicero,
)

UnitStr = Literal["millimeter", "point", "inch", "pica", "didot", "cicero"]


class PageLayout(QtGui.QPageLayout):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def serialize_fields(self):
        return dict(
            margins=self.margins(),
            minimum_margins=self.minimumMargins(),
            mode=self.get_mode(),
            orientation=self.get_orientation(),
            page_size=self.get_page_size(),
            units=self.get_units(),
        )

    def set_units(self, unit: UnitStr):
        """Set unit.

        Args:
            unit: unit

        Raises:
            InvalidParamError: unit does not exist
        """
        if unit not in UNITS:
            raise InvalidParamError(unit, UNITS)
        self.setUnits(UNITS[unit])

    def get_units(self) -> UnitStr:
        """Get the current unit.

        Returns:
            unit
        """
        return UNITS.inverse[self.units()]

    def set_mode(self, mode: ModeStr):
        """Set mode.

        Args:
            mode: mode

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.setMode(MODES[mode])

    def get_mode(self) -> ModeStr:
        """Get the current mode.

        Returns:
            mode
        """
        return MODES.inverse[self.mode()]

    def set_orientation(self, orientation: OrientationStr):
        """Set orientation.

        Args:
            orientation: orientation

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise InvalidParamError(orientation, ORIENTATIONS)
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> OrientationStr:
        """Get the current orientation.

        Returns:
            orientation
        """
        return ORIENTATIONS.inverse[self.orientation()]

    def get_page_size(self) -> gui.PageSize:
        return gui.PageSize(self.pageSize())


if __name__ == "__main__":
    movie = PageLayout()
