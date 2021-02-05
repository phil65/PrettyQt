from __future__ import annotations

from prettyqt import core, location
from prettyqt.qt import QtLocation


QtLocation.QGeoRoutingManager.__bases__ = (core.Object,)


class GeoRoutingManager:
    def __init__(self, item: QtLocation.QGeoRoutingManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_locale(self) -> core.Locale:
        return core.Locale(self.item.locale())

    def get_supported_feature_types(
        self,
    ) -> list[location.georouterequest.FeatureTypeStr]:
        return [
            k
            for k, v in location.georouterequest.FEATURE_TYPES.items()
            if v & self.item.supportedFeatureTypes()
        ]

    def get_supported_feature_weights(
        self,
    ) -> list[location.georouterequest.FeatureWeightStr]:
        return [
            k
            for k, v in location.georouterequest.FEATURE_WEIGHTS.items()
            if v & self.item.supportedFeatureWeights()
        ]

    def get_supported_maneuver_details(
        self,
    ) -> list[location.georouterequest.ManeuverDetailStr]:
        return [
            k
            for k, v in location.georouterequest.MANEUVER_DETAIL.items()
            if v & self.item.supportedManeuverDetails()
        ]

    def get_supported_route_optimizations(
        self,
    ) -> list[location.georouterequest.RouteOptimizationStr]:
        return location.georouterequest.ROUTE_OPTIMIZATION.get_list(
            self.item.supportedRouteOptimizations()
        )

    def get_supported_segment_details(
        self,
    ) -> list[location.georouterequest.SegmentDetailStr]:
        return [
            k
            for k, v in location.georouterequest.SEGMENT_DETAIL.items()
            if v & self.item.supportedSegmentDetails()
        ]

    def get_supported_travel_modes(self) -> list[location.georouterequest.TravelModeStr]:
        return [
            k
            for k, v in location.georouterequest.TRAVEL_MODE.items()
            if v & self.item.supportedTravelModes()
        ]
