# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy.QtCharts import QtCharts
from prettyqt import core


QtCharts.QAbstractSeries.__bases__ = (core.Object,)


class AbstractSeries(QtCharts.QAbstractSeries):

    """
    QAbstractSeries with some custom properties
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._group = ""

    @core.Property(object)
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value
