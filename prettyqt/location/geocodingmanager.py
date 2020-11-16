# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import core

QtLocation.QGeoCodingManager.__bases__ = (core.Object,)


class GeoCodingManager:
    def __init__(self, item: QtLocation.QGeoCodingManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_locale(self) -> core.Locale:
        return core.Locale(self.item.locale())
