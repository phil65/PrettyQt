# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError

MODES = bidict(
    standard=QtGui.QPageLayout.StandardMode, full_page=QtGui.QPageLayout.FullPageMode
)

ORIENTATIONS = bidict(
    portrait=QtGui.QPageLayout.Portrait, landscape=QtGui.QPageLayout.Landscape
)

UNITS = bidict(
    millimeter=QtGui.QPageLayout.Millimeter,
    point=QtGui.QPageLayout.Point,
    inch=QtGui.QPageLayout.Inch,
    pica=QtGui.QPageLayout.Pica,
    didot=QtGui.QPageLayout.Didot,
    cicero=QtGui.QPageLayout.Cicero,
)


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

    def set_units(self, unit: str):
        """Set unit.

        Valid values for units: "millimeter", "point", "inch", "pica", "didot", "cicero"

        Args:
            units: unit

        Raises:
            InvalidParamError: unit does not exist
        """
        if unit not in UNITS:
            raise InvalidParamError(unit, UNITS)
        self.setUnits(UNITS[unit])

    def get_units(self) -> str:
        """Get the current unit.

        Possible values: "millimeter", "point", "inch", "pica", "didot", "cicero"

        Returns:
            unit
        """
        return UNITS.inv[self.units()]

    def set_mode(self, mode: str):
        """Set mode.

        Valid values for mode: "standard", "full_page"

        Args:
            mode: mode

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.setMode(MODES[mode])

    def get_mode(self) -> str:
        """Get the current mode.

        Possible values: "standard", "full_page"

        Returns:
            mode
        """
        return MODES.inv[self.mode()]

    def set_orientation(self, orientation: str):
        """Set orientation.

        Valid values for orientation: "portrait", "landscape"

        Args:
            orientation: orientation

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in ORIENTATIONS:
            raise InvalidParamError(orientation, ORIENTATIONS)
        self.setOrientation(ORIENTATIONS[orientation])

    def get_orientation(self) -> str:
        """Get the current orientation.

        Possible values: "portrait", "landscape"

        Returns:
            orientation
        """
        return ORIENTATIONS.inv[self.orientation()]

    def get_page_size(self) -> gui.PageSize:
        return gui.PageSize(self.pageSize())


if __name__ == "__main__":
    movie = PageLayout()
