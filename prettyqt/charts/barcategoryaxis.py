from __future__ import annotations

from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QBarCategoryAxis.__bases__ = (charts.AbstractAxis,)


class BarCategoryAxis(QtCharts.QBarCategoryAxis):
    def __delitem__(self, index: str):
        self.remove(index)

    def __getitem__(self, index: int) -> str:
        return self.categories()[index]

    def __setitem__(self, index: str, value: str):
        self.replace(index, value)

    def __add__(self, other: str) -> BarCategoryAxis:
        self.append(other)
        return self
