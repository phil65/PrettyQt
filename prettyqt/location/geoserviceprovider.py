from __future__ import annotations

from typing import Literal

from prettyqt import core, location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


QGeoServiceProvider = QtLocation.QGeoServiceProvider

ERROR = bidict(
    none=QGeoServiceProvider.Error.NoError,
    not_supported=QGeoServiceProvider.Error.NotSupportedError,
    unknown_parameter=QGeoServiceProvider.Error.UnknownParameterError,
    missing_required_parameter=QGeoServiceProvider.Error.MissingRequiredParameterError,
    connection=QGeoServiceProvider.Error.ConnectionError,
    failed_to_load=QGeoServiceProvider.Error.LoaderError,
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
    none=QGeoServiceProvider.GeocodingFeature.NoGeocodingFeatures,
    online=QGeoServiceProvider.GeocodingFeature.OnlineGeocodingFeature,
    offline=QGeoServiceProvider.GeocodingFeature.OfflineGeocodingFeature,
    reverse=QGeoServiceProvider.GeocodingFeature.ReverseGeocodingFeature,
    localized=QGeoServiceProvider.GeocodingFeature.LocalizedGeocodingFeature,
    # any=QGeoServiceProvider.GeocodingFeature.AnyGeocodingFeatures,
)

GeocodingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "reverse",
    "localized",
]

MAPPING_FEATURES = bidict(
    none=QGeoServiceProvider.MappingFeature.NoMappingFeatures,
    online=QGeoServiceProvider.MappingFeature.OnlineMappingFeature,
    offline=QGeoServiceProvider.MappingFeature.OfflineMappingFeature,
    localized=QGeoServiceProvider.MappingFeature.LocalizedMappingFeature,
    # any=QGeoServiceProvider.MappingFeature.AnyMappingFeatures,
)

MappingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "localized",
]

NAVIGATION_FEATURES = bidict(
    none=QGeoServiceProvider.NavigationFeature.NoNavigationFeatures,
    online=QGeoServiceProvider.NavigationFeature.OnlineNavigationFeature,
    offline=QGeoServiceProvider.NavigationFeature.OfflineNavigationFeature,
    # any=QGeoServiceProvider.NavigationFeature.AnyNavigationFeatures,
)

NavigationFeatureStr = Literal[
    "none",
    "online",
    "offline",
]

PLACES_FEATURES = bidict(
    none=QGeoServiceProvider.PlacesFeature.NoPlacesFeatures,
    online_places=QGeoServiceProvider.PlacesFeature.OnlinePlacesFeature,
    offline_places=QGeoServiceProvider.PlacesFeature.OfflinePlacesFeature,
    save_place=QGeoServiceProvider.PlacesFeature.SavePlaceFeature,
    remove_place=QGeoServiceProvider.PlacesFeature.RemovePlaceFeature,
    save_category=QGeoServiceProvider.PlacesFeature.SaveCategoryFeature,
    remove_category=QGeoServiceProvider.PlacesFeature.RemoveCategoryFeature,
    place_recommendations=QGeoServiceProvider.PlacesFeature.PlaceRecommendationsFeature,
    search_suggestions=QGeoServiceProvider.PlacesFeature.SearchSuggestionsFeature,
    localized_places=QGeoServiceProvider.PlacesFeature.LocalizedPlacesFeature,
    notifications=QGeoServiceProvider.PlacesFeature.NotificationsFeature,
    place_matching=QGeoServiceProvider.PlacesFeature.PlaceMatchingFeature,
    # any=QGeoServiceProvider.PlacesFeature.AnyPlacesFeatures,
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
    none=QGeoServiceProvider.RoutingFeature.NoRoutingFeatures,
    online=QGeoServiceProvider.RoutingFeature.OnlineRoutingFeature,
    offline=QGeoServiceProvider.RoutingFeature.OfflineRoutingFeature,
    localized=QGeoServiceProvider.RoutingFeature.LocalizedRoutingFeature,
    route_updates=QGeoServiceProvider.RoutingFeature.RouteUpdatesFeature,
    alternative_routes=QGeoServiceProvider.RoutingFeature.AlternativeRoutesFeature,
    exclude_areas=QGeoServiceProvider.RoutingFeature.ExcludeAreasRoutingFeature,
    # any=QtLocation.QGeoServiceProvider.RoutingFeature.AnyRoutingFeatures,
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


class GeoServiceProvider(core.ObjectMixin, QtLocation.QGeoServiceProvider):
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
