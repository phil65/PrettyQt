from typing import List

from qtpy import QtLocation

from prettyqt import core, positioning
from prettyqt.utils import InvalidParamError, bidict, helpers, mappers


FEATURE_TYPES = bidict(
    none=QtLocation.QGeoRouteRequest.NoFeature,
    toll=QtLocation.QGeoRouteRequest.TollFeature,
    highway=QtLocation.QGeoRouteRequest.HighwayFeature,
    public_transit=QtLocation.QGeoRouteRequest.PublicTransitFeature,
    ferry=QtLocation.QGeoRouteRequest.FerryFeature,
    tunnel=QtLocation.QGeoRouteRequest.TunnelFeature,
    dirt_road=QtLocation.QGeoRouteRequest.DirtRoadFeature,
    parks=QtLocation.QGeoRouteRequest.ParksFeature,
    motor_pool_lane=QtLocation.QGeoRouteRequest.MotorPoolLaneFeature,
    traffic=QtLocation.QGeoRouteRequest.TrafficFeature,
)

FEATURE_WEIGHTS = bidict(
    neutral=QtLocation.QGeoRouteRequest.NeutralFeatureWeight,
    prefer=QtLocation.QGeoRouteRequest.PreferFeatureWeight,
    require=QtLocation.QGeoRouteRequest.RequireFeatureWeight,
    avoid=QtLocation.QGeoRouteRequest.AvoidFeatureWeight,
    disallow=QtLocation.QGeoRouteRequest.DisallowFeatureWeight,
)

MANEUVER_DETAIL = bidict(
    none=QtLocation.QGeoRouteRequest.NoManeuvers,
    basic=QtLocation.QGeoRouteRequest.BasicManeuvers,
)

ROUTE_OPTIMIZATION = mappers.FlagMap(
    QtLocation.QGeoRouteRequest.RouteOptimizations,
    shortest=QtLocation.QGeoRouteRequest.ShortestRoute,
    fastest=QtLocation.QGeoRouteRequest.FastestRoute,
    most_economic=QtLocation.QGeoRouteRequest.MostEconomicRoute,
    most_scenic=QtLocation.QGeoRouteRequest.MostScenicRoute,
)

SEGMENT_DETAIL = bidict(
    none=QtLocation.QGeoRouteRequest.NoSegmentData,
    basic=QtLocation.QGeoRouteRequest.BasicSegmentData,
)

TRAVEL_MODE = bidict(
    car=QtLocation.QGeoRouteRequest.CarTravel,
    pedestrian=QtLocation.QGeoRouteRequest.PedestrianTravel,
    bicycle=QtLocation.QGeoRouteRequest.BicycleTravel,
    public_transit=QtLocation.QGeoRouteRequest.PublicTransitTravel,
    truck=QtLocation.QGeoRouteRequest.TruckTravel,
)


class GeoRouteRequest(QtLocation.QGeoRouteRequest):
    def get_waypoints(self) -> List[positioning.GeoCoordinate]:
        return [positioning.GeoCoordinate(wp) for wp in self.waypoints()]

    def get_exclude_areas(self) -> List[positioning.GeoRectangle]:
        return [positioning.GeoRectangle(wp) for wp in self.excludeAreas()]

    def get_departure_time(self) -> core.DateTime:
        return core.DateTime(self.departureTime())

    def set_feature_weight(self, feature: str, weight: str):
        """Set the feature weight.

        Allowed values for weight: "neutral", "prefer", "require", "avoid", "disallow"

        Args:
            feature: Feature type
            weight: Feature weight

        Raises:
            InvalidParamError: feature weight / type does not exist
        """
        if weight not in FEATURE_WEIGHTS:
            raise InvalidParamError(weight, FEATURE_WEIGHTS)
        if feature not in FEATURE_TYPES:
            raise InvalidParamError(feature, FEATURE_TYPES)
        self.setFeatureWeight(FEATURE_TYPES[feature], FEATURE_WEIGHTS[weight])

    def get_feature_weight(self, feature: str) -> str:
        """Return current feature weight.

        Possible values for weight: "neutral", "prefer", "require", "avoid", "disallow"

        Returns:
            Feature weight
        """
        if feature not in FEATURE_TYPES:
            raise InvalidParamError(feature, FEATURE_TYPES)
        return FEATURE_WEIGHTS.inverse[self.featureWeight(FEATURE_TYPES[feature])]

    def set_route_optimization(self, optimization: str):
        """Set the route optimization.

        Allowed values are "shortest", "fastest", "most_economic", "most_scenic"

        Args:
            optimization: Route optimization

        Raises:
            InvalidParamError: route optimization does not exist
        """
        if optimization not in ROUTE_OPTIMIZATION:
            raise InvalidParamError(optimization, ROUTE_OPTIMIZATION)
        self.setRouteOptimization(ROUTE_OPTIMIZATION[optimization])

    def get_route_optimization(self) -> str:
        """Return current route optimization.

        Possible values: "shortest", "fastest", "most_economic", "most_scenic"

        Returns:
            Route optimization
        """
        return ROUTE_OPTIMIZATION.inverse[self.routeOptimization()]

    def get_travel_modes(self) -> List[str]:
        return [k for k, v in TRAVEL_MODE.items() if v & self.travelModes()]

    def set_travel_modes(self, *mode: str):
        for item in mode:
            if item not in TRAVEL_MODE:
                raise InvalidParamError(item, TRAVEL_MODE)
        flags = helpers.merge_flags(mode, TRAVEL_MODE)
        self.setTravelModes(flags)

    def get_feature_types(self) -> List[str]:
        return [k for k, v in FEATURE_TYPES.items() for t in self.featureTypes() if v & t]


if __name__ == "__main__":
    request = GeoRouteRequest()
