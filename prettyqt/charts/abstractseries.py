from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCharts


class AbstractSeriesMixin(core.ObjectMixin):
    pass


class AbstractSeries(AbstractSeriesMixin, QtCharts.QAbstractSeries):
    pass
