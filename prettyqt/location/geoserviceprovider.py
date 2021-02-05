from __future__ import annotations

from typing import Literal

from prettyqt import core, location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


QGeoServiceProvider = QtLocation.QGeoServiceProvider

ERROR = bidict(
    none=QGeoServiceProvider.NoError,
    not_supported=QGeoServiceProvider.NotSupportedError,
    unknown_parameter=QGeoServiceProvider.UnknownParameterError,
    missing_required_parameter=QGeoServiceProvider.MissingRequiredParameterError,
    connection=QGeoServiceProvider.ConnectionError,
    failed_to_load=QGeoServiceProvider.LoaderError,
)

ErrorStr = Literal[
    "none",
    "not_supported",
    "unknown_parameter",
    "missing_required_parameter",
    "connection",
    "failed_to_load",
]

GEOCODING_FEATURES = bidict(
    none=QtLocation.QGeoServiceProvider.NoGeocodingFeatures,
    online=QtLocation.QGeoServiceProvider.OnlineGeocodingFeature,
    offline=QtLocation.QGeoServiceProvider.OfflineGeocodingFeature,
    reverse=QtLocation.QGeoServiceProvider.ReverseGeocodingFeature,
    localized=QtLocation.QGeoServiceProvider.LocalizedGeocodingFeature,
    # any=QtLocation.QGeoServiceProvider.AnyGeocodingFeatures,
)

GeocodingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "reverse",
    "localized",
]

MAPPING_FEATURES = bidict(
    none=QtLocation.QGeoServiceProvider.NoMappingFeatures,
    online=QtLocation.QGeoServiceProvider.OnlineMappingFeature,
    offline=QtLocation.QGeoServiceProvider.OfflineMappingFeature,
    localized=QtLocation.QGeoServiceProvider.LocalizedMappingFeature,
    # any=QtLocation.QGeoServiceProvider.AnyMappingFeatures,
)

MappingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "localized",
]

NAVIGATION_FEATURES = bidict(
    none=QtLocation.QGeoServiceProvider.NoNavigationFeatures,
    online=QtLocation.QGeoServiceProvider.OnlineNavigationFeature,
    offline=QtLocation.QGeoServiceProvider.OfflineNavigationFeature,
    # any=QtLocation.QGeoServiceProvider.AnyNavigationFeatures,
)

NavigationFeatureStr = Literal[
    "none",
    "online",
    "offline",
]

PLACES_FEATURES = bidict(
    none=QtLocation.QGeoServiceProvider.NoPlacesFeatures,
    online_places=QtLocation.QGeoServiceProvider.OnlinePlacesFeature,
    offline_places=QtLocation.QGeoServiceProvider.OfflinePlacesFeature,
    save_place=QtLocation.QGeoServiceProvider.SavePlaceFeature,
    remove_place=QtLocation.QGeoServiceProvider.RemovePlaceFeature,
    save_category=QtLocation.QGeoServiceProvider.SaveCategoryFeature,
    remove_category=QtLocation.QGeoServiceProvider.RemoveCategoryFeature,
    place_recommendations=QtLocation.QGeoServiceProvider.PlaceRecommendationsFeature,
    search_suggestions=QtLocation.QGeoServiceProvider.SearchSuggestionsFeature,
    localized_places=QtLocation.QGeoServiceProvider.LocalizedPlacesFeature,
    notifications=QtLocation.QGeoServiceProvider.NotificationsFeature,
    place_matching=QtLocation.QGeoServiceProvider.PlaceMatchingFeature,
    # any=QtLocation.QGeoServiceProvider.AnyPlacesFeatures,
)

PlaceFeatureStr = Literal[
    "none",
    "online_places",
    "offline_places",
    "save_place",
    "remove_place",
    "save_category",
    "remove_category",
    "place_recommendations",
    "search_suggestions",
    "localized_places",
    "notifications",
    "place_matching",
]

ROUTING_FEATURES = bidict(
    none=QtLocation.QGeoServiceProvider.NoRoutingFeatures,
    online=QtLocation.QGeoServiceProvider.OnlineRoutingFeature,
    offline=QtLocation.QGeoServiceProvider.OfflineRoutingFeature,
    localized=QtLocation.QGeoServiceProvider.LocalizedRoutingFeature,
    route_updates=QtLocation.QGeoServiceProvider.RouteUpdatesFeature,
    alternative_routes=QtLocation.QGeoServiceProvider.AlternativeRoutesFeature,
    exclude_areas=QtLocation.QGeoServiceProvider.ExcludeAreasRoutingFeature,
    # any=QtLocation.QGeoServiceProvider.AnyRoutingFeatures,
)

RoutingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "localized",
    "route_updates",
    "alternative_routes",
    "exclude_areas",
]

QtLocation.QGeoServiceProvider.__bases__ = (core.Object,)


class GeoServiceProvider(QtLocation.QGeoServiceProvider):
    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def get_geocoding_error(self) -> ErrorStr:
        return ERROR.inverse[self.geocodingError()]

    def get_geocoding_features(self) -> list[GeocodingFeatureStr]:
        return [k for k, v in GEOCODING_FEATURES.items() if v & self.geocodingFeatures()]

    def get_mapping_error(self) -> ErrorStr:
        return ERROR.inverse[self.mappingError()]

    def get_mapping_features(self) -> list[MappingFeatureStr]:
        return [k for k, v in MAPPING_FEATURES.items() if v & self.mappingFeatures()]

    def get_navigation_error(self) -> ErrorStr:
        return ERROR.inverse[self.navigationError()]

    def get_navigation_features(self) -> list[NavigationFeatureStr]:
        return [
            k for k, v in NAVIGATION_FEATURES.items() if v & self.navigationFeatures()
        ]

    def get_places_error(self) -> ErrorStr:
        return ERROR.inverse[self.placesError()]

    def get_places_features(self) -> list[PlaceFeatureStr]:
        return [k for k, v in PLACES_FEATURES.items() if v & self.placesFeatures()]

    def get_routing_error(self) -> ErrorStr:
        return ERROR.inverse[self.routingError()]

    def get_routing_features(self) -> list[RoutingFeatureStr]:
        return [k for k, v in ROUTING_FEATURES.items() if v & self.routingFeatures()]

    def get_geocoding_manager(self) -> location.GeoCodingManager:
        return location.GeoCodingManager(self.geocodingManager())

    def get_routing_manager(self) -> location.GeoRoutingManager:
        return location.GeoRoutingManager(self.routingManager())

    def get_place_manager(self) -> location.PlaceManager:
        return location.PlaceManager(self.placeManager())
