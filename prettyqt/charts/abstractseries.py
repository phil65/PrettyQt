from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCharts


class AbstractSeriesMixin(core.ObjectMixin):
    """QAbstractSeries with some custom properties."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._group = ""

    def get_group(self):
        return self._group

    def set_group(self, value):
        self._group = value

    group = core.Property(str, get_group, set_group)


class AbstractSeries(AbstractSeriesMixin, QtCharts.QAbstractSeries):
    pass
