from __future__ import annotations

from typing import Literal

from prettyqt import core, positioning
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


FeatureTypeStr = Literal[
    "none",
    "toll",
    "highway",
    "public_transit",
    "ferry",
    "tunnel",
    "dirt_road",
    "parks",
    "motor_pool_lane",
    "traffic",
]

FEATURE_TYPES: bidict[FeatureTypeStr, QtLocation.QGeoRouteRequest.FeatureType] = bidict(
    none=QtLocation.QGeoRouteRequest.FeatureType.NoFeature,
    toll=QtLocation.QGeoRouteRequest.FeatureType.TollFeature,
    highway=QtLocation.QGeoRouteRequest.FeatureType.HighwayFeature,
    public_transit=QtLocation.QGeoRouteRequest.FeatureType.PublicTransitFeature,
    ferry=QtLocation.QGeoRouteRequest.FeatureType.FerryFeature,
    tunnel=QtLocation.QGeoRouteRequest.FeatureType.TunnelFeature,
    dirt_road=QtLocation.QGeoRouteRequest.FeatureType.DirtRoadFeature,
    parks=QtLocation.QGeoRouteRequest.FeatureType.ParksFeature,
    motor_pool_lane=QtLocation.QGeoRouteRequest.FeatureType.MotorPoolLaneFeature,
    traffic=QtLocation.QGeoRouteRequest.FeatureType.TrafficFeature,
)

FeatureWeightStr = Literal["neutral", "prefer", "require", "avoid", "disallow"]

FEATURE_WEIGHTS: bidict[FeatureWeightStr, QtLocation.QGeoRouteRequest.FeatureWeight] = (
    bidict(
        neutral=QtLocation.QGeoRouteRequest.FeatureWeight.NeutralFeatureWeight,
        prefer=QtLocation.QGeoRouteRequest.FeatureWeight.PreferFeatureWeight,
        require=QtLocation.QGeoRouteRequest.FeatureWeight.RequireFeatureWeight,
        avoid=QtLocation.QGeoRouteRequest.FeatureWeight.AvoidFeatureWeight,
        disallow=QtLocation.QGeoRouteRequest.FeatureWeight.DisallowFeatureWeight,
    )
)

ManeuverDetailStr = Literal["none", "basic"]

MANEUVER_DETAIL: bidict[ManeuverDetailStr, QtLocation.QGeoRouteRequest.ManeuverDetail] = (
    bidict(
        none=QtLocation.QGeoRouteRequest.ManeuverDetail.NoManeuvers,
        basic=QtLocation.QGeoRouteRequest.ManeuverDetail.BasicManeuvers,
    )
)

RouteOptimizationStr = Literal["shortest", "fastest", "most_economic", "most_scenic"]

ROUTE_OPTIMIZATION: bidict[
    RouteOptimizationStr, QtLocation.QGeoRouteRequest.RouteOptimization
] = bidict(
    shortest=QtLocation.QGeoRouteRequest.RouteOptimization.ShortestRoute,
    fastest=QtLocation.QGeoRouteRequest.RouteOptimization.FastestRoute,
    most_economic=QtLocation.QGeoRouteRequest.RouteOptimization.MostEconomicRoute,
    most_scenic=QtLocation.QGeoRouteRequest.RouteOptimization.MostScenicRoute,
)

SegmentDetailStr = Literal["none", "basic"]

SEGMENT_DETAIL: bidict[SegmentDetailStr, QtLocation.QGeoRouteRequest.SegmentDetail] = (
    bidict(
        none=QtLocation.QGeoRouteRequest.SegmentDetail.NoSegmentData,
        basic=QtLocation.QGeoRouteRequest.SegmentDetail.BasicSegmentData,
    )
)

TravelModeStr = Literal["car", "pedestrian", "bicycle", "public_transit", "truck"]

TRAVEL_MODE: bidict[TravelModeStr, QtLocation.QGeoRouteRequest.TravelMode] = bidict(
    car=QtLocation.QGeoRouteRequest.TravelMode.CarTravel,
    pedestrian=QtLocation.QGeoRouteRequest.TravelMode.PedestrianTravel,
    bicycle=QtLocation.QGeoRouteRequest.TravelMode.BicycleTravel,
    public_transit=QtLocation.QGeoRouteRequest.TravelMode.PublicTransitTravel,
    truck=QtLocation.QGeoRouteRequest.TravelMode.TruckTravel,
)


class GeoRouteRequest(QtLocation.QGeoRouteRequest):
    """Represents the params and restrictions defining a routing information request."""

    def get_waypoints(self) -> list[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(wp) for wp in self.waypoints()]

    def get_exclude_areas(self) -> list[positioning.GeoRectangle]:
        return [positioning.GeoRectangle(wp) for wp in self.excludeAreas()]

    def get_departure_time(self) -> core.DateTime:
        return core.DateTime(self.departureTime())

    def set_feature_weight(
        self,
        feature: FeatureTypeStr | QtLocation.QGeoRouteRequest.FeatureType,
        weight: FeatureWeightStr | QtLocation.QGeoRouteRequest.FeatureWeight,
    ):
        """Set the feature weight.

        Args:
            feature: Feature type
            weight: Feature weight
        """
        self.setFeatureWeight(
            FEATURE_TYPES.get_enum_value(feature), FEATURE_WEIGHTS.get_enum_value(weight)
        )

    def get_feature_weight(
        self, feature: FeatureTypeStr | QtLocation.QGeoRouteRequest.FeatureType
    ) -> FeatureWeightStr:
        """Return current feature weight.

        Returns:
            Feature weight
        """
        return FEATURE_WEIGHTS.inverse[
            self.featureWeight(FEATURE_TYPES.get_enum_value(feature))
        ]

    def set_route_optimization(
        self,
        optimization: RouteOptimizationStr
        | QtLocation.QGeoRouteRequest.RouteOptimization,
    ):
        """Set the route optimization.

        Args:
            optimization: Route optimization
        """
        self.setRouteOptimization(ROUTE_OPTIMIZATION.get_enum_value(optimization))

    def get_route_optimization(self) -> RouteOptimizationStr:
        """Return current route optimization.

        Returns:
            Route optimization
        """
        return ROUTE_OPTIMIZATION.inverse[self.routeOptimization()]

    def get_travel_modes(self) -> list[TravelModeStr]:
        return TRAVEL_MODE.get_list(self.travelModes())

    def set_travel_modes(self, *mode: TravelModeStr):
        flags = TRAVEL_MODE.merge_flags(mode)
        self.setTravelModes(flags)

    def get_feature_types(self) -> list[FeatureTypeStr]:
        return [k for k, v in FEATURE_TYPES.items() for t in self.featureTypes() if v & t]


if __name__ == "__main__":
    request = GeoRouteRequest()
