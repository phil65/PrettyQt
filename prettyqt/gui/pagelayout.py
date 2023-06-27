from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.utils import bidict, get_repr


ModeStr = Literal["standard", "full_page"]

MODES: bidict[ModeStr, gui.QPageLayout.Mode] = bidict(
    standard=gui.QPageLayout.Mode.StandardMode,
    full_page=gui.QPageLayout.Mode.FullPageMode,
)

OrientationStr = Literal["portrait", "landscape"]

ORIENTATIONS: bidict[OrientationStr, gui.QPageLayout.Orientation] = bidict(
    portrait=gui.QPageLayout.Orientation.Portrait,
    landscape=gui.QPageLayout.Orientation.Landscape,
)

UnitStr = Literal["millimeter", "point", "inch", "pica", "didot", "cicero"]

UNITS: bidict[UnitStr, gui.QPageLayout.Unit] = bidict(
    millimeter=gui.QPageLayout.Unit.Millimeter,
    point=gui.QPageLayout.Unit.Point,
    inch=gui.QPageLayout.Unit.Inch,
    pica=gui.QPageLayout.Unit.Pica,
    didot=gui.QPageLayout.Unit.Didot,
    cicero=gui.QPageLayout.Unit.Cicero,
)


class PageLayout(gui.QPageLayout):
    def __repr__(self):
        return get_repr(self)

    def set_units(self, unit: UnitStr | gui.QPageLayout.Unit):
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

    def set_mode(self, mode: ModeStr | gui.QPageLayout.Mode):
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
        self, orientation: OrientationStr | gui.QPageLayout.Orientation
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
