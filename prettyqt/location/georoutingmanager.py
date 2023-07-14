from __future__ import annotations

from prettyqt import core, location


class GeoRoutingManager(core.ObjectMixin):
    """Support for geographic routing operations."""

    def __init__(self, item: location.QGeoRoutingManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_locale(self) -> core.Locale:
        return core.Locale(self.item.locale())

    def get_supported_feature_types(
        self,
    ) -> list[location.georouterequest.FeatureTypeStr]:
        return location.georouterequest.FEATURE_TYPES.get_list(
            self.item.supportedFeatureTypes()
        )

    def get_supported_feature_weights(
        self,
    ) -> list[location.georouterequest.FeatureWeightStr]:
        return location.georouterequest.FEATURE_WEIGHTS.get_list(
            self.item.supportedFeatureWeights()
        )

    def get_supported_maneuver_details(
        self,
    ) -> list[location.georouterequest.ManeuverDetailStr]:
        return location.georouterequest.MANEUVER_DETAIL.get_list(
            self.item.supportedManeuverDetails()
        )

    def get_supported_route_optimizations(
        self,
    ) -> list[location.georouterequest.RouteOptimizationStr]:
        return location.georouterequest.ROUTE_OPTIMIZATION.get_list(
            self.item.supportedRouteOptimizations()
        )

    def get_supported_segment_details(
        self,
    ) -> list[location.georouterequest.SegmentDetailStr]:
        return location.georouterequest.SEGMENT_DETAIL.get_list(
            self.item.supportedSegmentDetails()
        )

    def get_supported_travel_modes(self) -> list[location.georouterequest.TravelModeStr]:
        return location.georouterequest.TRAVEL_MODE.get_list(
            self.item.supportedTravelModes()
        )
