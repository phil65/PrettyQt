# -*- coding: utf-8 -*-

from typing import List

from qtpy import QtLocation

from prettyqt import core, location

FEATURE_TYPES = location.georouterequest.FEATURE_TYPES
FEATURE_WEIGHTS = location.georouterequest.FEATURE_WEIGHTS
MANEUVER_DETAIL = location.georouterequest.MANEUVER_DETAIL
ROUTE_OPTIMIZATION = location.georouterequest.ROUTE_OPTIMIZATION
SEGMENT_DETAIL = location.georouterequest.SEGMENT_DETAIL
TRAVEL_MODE = location.georouterequest.TRAVEL_MODE


QtLocation.QPlaceManager.__bases__ = (core.Object,)


class PlaceManager:
    def __init__(self, item: QtLocation.QPlaceManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_category(self, cat_id: str) -> location.PlaceCategory:
        return location.PlaceCategory(self.item.category(cat_id))

    def get_child_categories(self, cat_id: str) -> List[location.PlaceCategory]:
        return [location.PlaceCategory(i) for i in self.item.childCategories(cat_id)]

    def get_locales(self) -> List[core.Locale]:
        return [core.Locale(i) for i in self.locales()]
