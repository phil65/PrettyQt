from __future__ import annotations

from qtpy import QtCore
from qtpy.QtCharts import QtCharts

from prettyqt import charts, gui


QtCharts.QXYSeries.__bases__ = (charts.AbstractSeries,)


class XYSeries(QtCharts.QXYSeries):
    """QXYSeries with some custom properties."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._process_name = ""
        self.setUseOpenGL()

    def __setitem__(self, index: int, val: QtCore.QPointF):
        self.replace(index, val)

    def __delitem__(self, index: int):
        self.remove(index)

    def __setstate__(self, state):
        self.append(state["points"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __add__(self, other: QtCore.QPointF) -> XYSeries:
        self.append(other)
        return self

    def serialize_fields(self):
        return dict(points=self.pointsVector())

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())
