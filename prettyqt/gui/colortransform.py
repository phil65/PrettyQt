from typing import TYPE_CHECKING

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import colors, get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class ColorTransform(QtGui.QColorTransform):
    """Transformation between color spaces."""

    def __repr__(self):
        return get_repr(self)

    def map_color(self, color: datatypes.ColorType) -> gui.Color:
        """Apply the color transformation to a color."""
        return gui.Color(self.map(colors.get_color(color)))


if __name__ == "__main__":
    transform = ColorTransform()
    print(repr(transform), transform.isIdentity())
