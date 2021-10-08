from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionSlider.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSlider(QtWidgets.QStyleOptionSlider):
    def is_horizontal(self) -> bool:
        """Check if silder is horizontal.

        Returns:
            True if horizontal, else False
        """
        return self.orientation == constants.HORIZONTAL

    def is_vertical(self) -> bool:
        """Check if silder is vertical.

        Returns:
            True if vertical, else False
        """
        return self.orientation == constants.VERTICAL

    def set_horizontal(self) -> None:
        """Set slider orientation to horizontal."""
        self.orientation = constants.HORIZONTAL

    def set_vertical(self) -> None:
        """Set slider orientation to vertical."""
        self.orientation = constants.VERTICAL

    def get_orientation(self) -> Literal["horizontal", "vertical"]:
        return "horizontal" if self.is_horizontal() else "vertical"
