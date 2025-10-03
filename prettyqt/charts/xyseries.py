from __future__ import annotations

from typing import TYPE_CHECKING

import prettyqt
from prettyqt import charts, gui
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    from prettyqt import core


class XYSeriesMixin(charts.AbstractSeriesMixin):
    def __setitem__(self, index: int, val: datatypes.PointFType):
        """Set point at given index to value."""
        self.replace(index, datatypes.to_pointf(val))

    def __delitem__(self, index: int):
        """Remove point with given index."""
        self.remove(index)

    # def __setstate__(self, state):
    #     self.append(state["points"])

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __add__(self, other: datatypes.PointFType) -> XYSeries:
        """Append a point to the Series."""
        self.append(datatypes.to_pointf(other))
        return self

    def get_points(self) -> list[core.QPoint]:
        if prettyqt.qt.API == "pyqt6":
            return [self.at(i) for i in range(self.count())]
        return self.points()

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


class XYSeries(XYSeriesMixin, charts.QXYSeries):
    pass
