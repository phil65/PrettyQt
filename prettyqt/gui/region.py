from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


REGION_TYPE = bidict(
    rectangle=QtGui.QRegion.RegionType.Rectangle,
    ellipse=QtGui.QRegion.RegionType.Ellipse,
)

RegionTypeStr = Literal["rectangle", "ellipse"]


class Region(QtGui.QRegion):
    def __repr__(self):
        return get_repr(self, self.get_bounding_rect(), self.get_shape())

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return ba.data()

    def get_bounding_rect(self) -> core.Rect:
        return core.Rect(self.boundingRect())

    def get_shape(self) -> RegionTypeStr:  # workaround for not being able to get shape
        return "rectangle" if self == Region(self.get_bounding_rect()) else "ellipse"


if __name__ == "__main__":
    region = Region(0, 0, 10, 10)
    print(repr(region))
