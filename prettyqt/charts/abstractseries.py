from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtCharts


if TYPE_CHECKING:
    _AbstractSeriesBase = QtCharts.QAbstractSeries
else:
    _AbstractSeriesBase = object


class AbstractSeriesMixin(core.ObjectMixin, _AbstractSeriesBase):
    pass


class AbstractSeries(AbstractSeriesMixin, QtCharts.QAbstractSeries):
    pass
