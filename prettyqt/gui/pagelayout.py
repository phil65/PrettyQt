from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


ModeStr = Literal["standard", "full_page"]

MODES: bidict[ModeStr, QtGui.QPageLayout.Mode] = bidict(
    standard=QtGui.QPageLayout.Mode.StandardMode,
    full_page=QtGui.QPageLayout.Mode.FullPageMode,
)

OrientationStr = Literal["portrait", "landscape"]

ORIENTATIONS: bidict[OrientationStr, QtGui.QPageLayout.Orientation] = bidict(
    portrait=QtGui.QPageLayout.Orientation.Portrait,
    landscape=QtGui.QPageLayout.Orientation.Landscape,
)

UnitStr = Literal["millimeter", "point", "inch", "pica", "didot", "cicero"]

UNITS: bidict[UnitStr, QtGui.QPageLayout.Unit] = bidict(
    millimeter=QtGui.QPageLayout.Unit.Millimeter,
    point=QtGui.QPageLayout.Unit.Point,
    inch=QtGui.QPageLayout.Unit.Inch,
    pica=QtGui.QPageLayout.Unit.Pica,
    didot=QtGui.QPageLayout.Unit.Didot,
    cicero=QtGui.QPageLayout.Unit.Cicero,
)


class PageLayout(QtGui.QPageLayout):
    def __repr__(self):
        return get_repr(self)

    def set_units(self, unit: UnitStr | QtGui.QPageLayout.Unit):
        """Set unit.

        Args:
            unit: unit
        """
        self.setUnits(UNITS.get_enum_value(unit))

    def get_units(self) -> UnitStr:
        """Get the current unit.

        Returns:
            unit
        """
        return UNITS.inverse[self.units()]

    def set_mode(self, mode: ModeStr | QtGui.QPageLayout.Mode):
        """Set mode.

        Args:
            mode: mode
        """
        self.setMode(MODES.get_enum_value(mode))

    def get_mode(self) -> ModeStr:
        """Get the current mode.

        Returns:
            mode
        """
        return MODES.inverse[self.mode()]

    def set_orientation(
        self, orientation: OrientationStr | QtGui.QPageLayout.Orientation
    ):
        """Set orientation.

        Args:
            orientation: orientation
        """
        self.setOrientation(ORIENTATIONS.get_enum_value(orientation))

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
