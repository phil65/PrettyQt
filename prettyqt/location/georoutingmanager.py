from typing import List

from qtpy import QtLocation

from prettyqt import core, location


QtLocation.QGeoRoutingManager.__bases__ = (core.Object,)


class GeoRoutingManager:
    def __init__(self, item: QtLocation.QGeoRoutingManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_locale(self) -> core.Locale:
        return core.Locale(self.item.locale())

    def get_supported_feature_types(self) -> List[str]:
        return [
            k
            for k, v in location.georouterequest.FEATURE_TYPES.items()
            if v & self.item.supportedFeatureTypes()
        ]

    def get_supported_feature_weights(self) -> List[str]:
        return [
            k
            for k, v in location.georouterequest.FEATURE_WEIGHTS.items()
            if v & self.item.supportedFeatureWeights()
        ]

    def get_supported_maneuver_details(self) -> List[str]:
        return [
            k
            for k, v in location.georouterequest.MANEUVER_DETAIL.items()
            if v & self.item.supportedManeuverDetails()
        ]

    def get_supported_route_optimizations(self) -> List[str]:
        return location.georouterequest.ROUTE_OPTIMIZATION.get_list(
            self.item.supportedRouteOptimizations()
        )

    def get_supported_segment_details(self) -> List[str]:
        return [
            k
            for k, v in location.georouterequest.SEGMENT_DETAIL.items()
            if v & self.item.supportedSegmentDetails()
        ]

    def get_supported_travel_modes(self) -> List[str]:
        return [
            k
            for k, v in location.georouterequest.TRAVEL_MODE.items()
            if v & self.item.supportedTravelModes()
        ]
