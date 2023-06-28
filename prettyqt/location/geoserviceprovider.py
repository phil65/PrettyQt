from __future__ import annotations

from typing import Literal

from prettyqt import core, location
from prettyqt.utils import bidict


QGeoServiceProvider = location.QGeoServiceProvider

ErrorStr = Literal[
    "none",
    "not_supported",
    "unknown_parameter",
    "missing_required_parameter",
    "connection",
    "failed_to_load",
]

ERROR: bidict[ErrorStr, QGeoServiceProvider.Error] = bidict(
    none=QGeoServiceProvider.Error.NoError,
    not_supported=QGeoServiceProvider.Error.NotSupportedError,
    unknown_parameter=QGeoServiceProvider.Error.UnknownParameterError,
    missing_required_parameter=QGeoServiceProvider.Error.MissingRequiredParameterError,
    connection=QGeoServiceProvider.Error.ConnectionError,
    failed_to_load=QGeoServiceProvider.Error.LoaderError,
)

GeocodingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "reverse",
    "localized",
]

GEOCODING_FEATURES: bidict[
    GeocodingFeatureStr, QGeoServiceProvider.GeocodingFeature
] = bidict(
    none=QGeoServiceProvider.GeocodingFeature.NoGeocodingFeatures,
    online=QGeoServiceProvider.GeocodingFeature.OnlineGeocodingFeature,
    offline=QGeoServiceProvider.GeocodingFeature.OfflineGeocodingFeature,
    reverse=QGeoServiceProvider.GeocodingFeature.ReverseGeocodingFeature,
    localized=QGeoServiceProvider.GeocodingFeature.LocalizedGeocodingFeature,
    # any=QGeoServiceProvider.GeocodingFeature.AnyGeocodingFeatures,
)

MappingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "localized",
]

MAPPING_FEATURES: bidict[MappingFeatureStr, QGeoServiceProvider.MappingFeature] = bidict(
    none=QGeoServiceProvider.MappingFeature.NoMappingFeatures,
    online=QGeoServiceProvider.MappingFeature.OnlineMappingFeature,
    offline=QGeoServiceProvider.MappingFeature.OfflineMappingFeature,
    localized=QGeoServiceProvider.MappingFeature.LocalizedMappingFeature,
    # any=QGeoServiceProvider.MappingFeature.AnyMappingFeatures,
)

NavigationFeatureStr = Literal[
    "none",
    "online",
    "offline",
]

NAVIGATION_FEATURES: bidict[
    NavigationFeatureStr, QGeoServiceProvider.NavigationFeature
] = bidict(
    none=QGeoServiceProvider.NavigationFeature.NoNavigationFeatures,
    online=QGeoServiceProvider.NavigationFeature.OnlineNavigationFeature,
    offline=QGeoServiceProvider.NavigationFeature.OfflineNavigationFeature,
    # any=QGeoServiceProvider.NavigationFeature.AnyNavigationFeatures,
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

PLACES_FEATURES: bidict[PlaceFeatureStr, QGeoServiceProvider.PlacesFeature] = bidict(
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

RoutingFeatureStr = Literal[
    "none",
    "online",
    "offline",
    "localized",
    "route_updates",
    "alternative_routes",
    "exclude_areas",
]

ROUTING_FEATURES: bidict[RoutingFeatureStr, QGeoServiceProvider.RoutingFeature] = bidict(
    none=QGeoServiceProvider.RoutingFeature.NoRoutingFeatures,
    online=QGeoServiceProvider.RoutingFeature.OnlineRoutingFeature,
    offline=QGeoServiceProvider.RoutingFeature.OfflineRoutingFeature,
    localized=QGeoServiceProvider.RoutingFeature.LocalizedRoutingFeature,
    route_updates=QGeoServiceProvider.RoutingFeature.RouteUpdatesFeature,
    alternative_routes=QGeoServiceProvider.RoutingFeature.AlternativeRoutesFeature,
    exclude_areas=QGeoServiceProvider.RoutingFeature.ExcludeAreasRoutingFeature,
    # any=location.QGeoServiceProvider.RoutingFeature.AnyRoutingFeatures,
)


class GeoServiceProvider(core.ObjectMixin, location.QGeoServiceProvider):
    def get_error(self) -> ErrorStr:
        return ERROR.inverse[self.error()]

    def get_geocoding_error(self) -> ErrorStr:
        return ERROR.inverse[self.geocodingError()]

    def get_geocoding_features(self) -> list[GeocodingFeatureStr]:
        return GEOCODING_FEATURES.get_list(self.geocodingFeatures())

    def get_mapping_error(self) -> ErrorStr:
        return ERROR.inverse[self.mappingError()]

    def get_mapping_features(self) -> list[MappingFeatureStr]:
        return MAPPING_FEATURES.get_list(self.mappingFeatures())

    def get_navigation_error(self) -> ErrorStr:
        return ERROR.inverse[self.navigationError()]

    def get_navigation_features(self) -> list[NavigationFeatureStr]:
        return NAVIGATION_FEATURES.get_list(self.navigationFeatures())

    def get_places_error(self) -> ErrorStr:
        return ERROR.inverse[self.placesError()]

    def get_places_features(self) -> list[PlaceFeatureStr]:
        return PLACES_FEATURES.get_list(self.placesFeatures())

    def get_routing_error(self) -> ErrorStr:
        return ERROR.inverse[self.routingError()]

    def get_routing_features(self) -> list[RoutingFeatureStr]:
        return ROUTING_FEATURES.get_list(self.routingFeatures())

    def get_geocoding_manager(self) -> location.GeoCodingManager:
        return location.GeoCodingManager(self.geocodingManager())

    def get_routing_manager(self) -> location.GeoRoutingManager:
        return location.GeoRoutingManager(self.routingManager())

    def get_place_manager(self) -> location.PlaceManager:
        return location.PlaceManager(self.placeManager())
