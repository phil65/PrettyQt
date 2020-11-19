from qtpy import QtCore, QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionSlider.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSlider(QtWidgets.QStyleOptionSlider):
    def is_horizontal(self) -> bool:
        """Check if silder is horizontal.

        Returns:
            True if horizontal, else False
        """
        return self.orientation == QtCore.Qt.Horizontal

    def is_vertical(self) -> bool:
        """Check if silder is vertical.

        Returns:
            True if vertical, else False
        """
        return self.orientation == QtCore.Qt.Vertical

    def set_horizontal(self) -> None:
        """Set slider orientation to horizontal."""
        self.orientation = QtCore.Qt.Horizontal

    def set_vertical(self) -> None:
        """Set slider orientation to vertical."""
        self.orientation = QtCore.Qt.Vertical

    def get_orientation(self) -> str:
        return "horizontal" if self.is_horizontal() else "vertical"
