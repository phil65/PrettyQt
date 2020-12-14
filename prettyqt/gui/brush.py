from typing import Literal

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict

PATTERN = bidict(
    none=QtCore.Qt.NoBrush,
    solid=QtCore.Qt.SolidPattern,
    dense_1=QtCore.Qt.Dense1Pattern,
    dense_2=QtCore.Qt.Dense2Pattern,
    dense_3=QtCore.Qt.Dense3Pattern,
    dense_4=QtCore.Qt.Dense4Pattern,
    dense_5=QtCore.Qt.Dense5Pattern,
    dense_6=QtCore.Qt.Dense6Pattern,
    dense_7=QtCore.Qt.Dense7Pattern,
    horizontal=QtCore.Qt.HorPattern,
    vertical=QtCore.Qt.VerPattern,
    cross=QtCore.Qt.CrossPattern,
    backward_diagonal=QtCore.Qt.BDiagPattern,
    forward_diagonal=QtCore.Qt.FDiagPattern,
    crossing_diagonal=QtCore.Qt.DiagCrossPattern,
    linear_gradient=QtCore.Qt.LinearGradientPattern,
    conical_gradient=QtCore.Qt.ConicalGradientPattern,
    radial_gradient=QtCore.Qt.RadialGradientPattern,
    texture=QtCore.Qt.TexturePattern,
)

PatternStr = Literal[
    "none",
    "solid",
    "dense_1",
    "dense_2",
    "dense_3",
    "dense_4",
    "dense_5",
    "dense_6",
    "dense_7",
    "horizontal",
    "vertical",
    "cross",
    "backward_diagonal",
    "forward_diagonal",
    "crossing_diagonal",
    "linear_gradient",
    "conical_gradient",
    "radial_gradient",
    "texture",
]


class Brush(QtGui.QBrush):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_color()!r}, {self.get_style()!r})"

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def get_texture_image(self) -> gui.Image:
        return gui.Image(self.textureImage())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_style(self) -> PatternStr:
        return PATTERN.inv[self.style()]


if __name__ == "__main__":
    b = Brush()
    print(repr(b))
