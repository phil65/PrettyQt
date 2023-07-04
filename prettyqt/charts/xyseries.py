from __future__ import annotations

import prettyqt

from prettyqt import charts, gui
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class XYSeriesMixin(charts.AbstractSeriesMixin):
    """QXYSeries with some custom properties."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._process_name = ""
        self.setUseOpenGL()

    def __setitem__(self, index: int, val: datatypes.PointFType):
        """Set point at given index to value."""
        self.replace(index, datatypes.toPointF(val))

    def __delitem__(self, index: int):
        """Remove point with given index."""
        self.remove(index)

    # def __setstate__(self, state):
    #     self.append(state["points"])

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __add__(self, other: QtCore.QPointF) -> XYSeries:
        """Append a point to the Series."""
        self.append(other)
        return self

    def serialize_fields(self):
        if prettyqt.qt.API == "pyqt6":
            points = [self.at(i) for i in range(self.count())]
        else:
            points = self.points()
        return dict(points=points)

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


class XYSeries(XYSeriesMixin, charts.QXYSeries):
    pass
