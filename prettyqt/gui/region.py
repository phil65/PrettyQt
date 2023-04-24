from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr, serializemixin


REGION_TYPE = bidict(
    rectangle=QtGui.QRegion.RegionType.Rectangle,
    ellipse=QtGui.QRegion.RegionType.Ellipse,
)

RegionTypeStr = Literal["rectangle", "ellipse"]


class Region(serializemixin.SerializeMixin, QtGui.QRegion):
    def __repr__(self):
        return get_repr(self, self.get_bounding_rect(), self.get_shape())

    def get_bounding_rect(self) -> core.Rect:
        return core.Rect(self.boundingRect())

    def get_shape(self) -> RegionTypeStr:  # workaround for not being able to get shape
        return "rectangle" if self == Region(self.get_bounding_rect()) else "ellipse"


if __name__ == "__main__":
    region = Region(0, 0, 10, 10)
    print(repr(region))
