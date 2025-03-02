"""Provides interfaces to create location-aware applications."""

from __future__ import annotations

from prettyqt.qt.QtLocation import *  # noqa: F403

from .qlocation import VISIBILITY, VisibilityStr
from .georouterequest import GeoRouteRequest
from .placeattribute import PlaceAttribute
from .placeratings import PlaceRatings
from .placecontactdetail import PlaceContactDetail
from .placeicon import PlaceIcon
from .placesupplier import PlaceSupplier
from .placecategory import PlaceCategory
from .placeuser import PlaceUser
from .placecontent import PlaceContent, PlaceContentMixin

# from .placeimage import PlaceImage
# from .placereview import PlaceReview
# from .placeeditorial import PlaceEditorial

from .geocodingmanager import GeoCodingManager
from .georoutingmanager import GeoRoutingManager
from .geomaneuver import GeoManeuver
from .georoutesegment import GeoRouteSegment
from .georoute import GeoRoute, GeoRouteMixin
from .placesearchrequest import PlaceSearchRequest
from .placecontentrequest import PlaceContentRequest
from .place import Place
from .placematchrequest import PlaceMatchRequest
from .placesearchresult import PlaceSearchResult, PlaceSearchResultMixin
from .placeresult import PlaceResult
from .placeproposedsearchresult import PlaceProposedSearchResult
from .placereply import PlaceReply, PlaceReplyMixin
from .placesearchreply import PlaceSearchReply
from .placecontentreply import PlaceContentReply
from .placedetailsreply import PlaceDetailsReply
from .placematchreply import PlaceMatchReply
from .placeidreply import PlaceIdReply
from .placemanager import PlaceManager
from .geoserviceprovider import GeoServiceProvider
from prettyqt.qt import QtLocation

QT_MODULE = QtLocation

__all__ = [
    "VISIBILITY",
    # "PlaceImage",
    # "PlaceReview",
    # "PlaceEditorial",
    "GeoCodingManager",
    "GeoManeuver",
    "GeoRoute",
    "GeoRouteMixin",
    "GeoRouteRequest",
    "GeoRouteSegment",
    "GeoRoutingManager",
    "GeoServiceProvider",
    "Place",
    "PlaceAttribute",
    "PlaceCategory",
    "PlaceContactDetail",
    "PlaceContent",
    "PlaceContentMixin",
    "PlaceContentReply",
    "PlaceContentRequest",
    "PlaceDetailsReply",
    "PlaceIcon",
    "PlaceIdReply",
    "PlaceManager",
    "PlaceMatchReply",
    "PlaceMatchRequest",
    "PlaceProposedSearchResult",
    "PlaceRatings",
    "PlaceReply",
    "PlaceReplyMixin",
    "PlaceResult",
    "PlaceSearchReply",
    "PlaceSearchRequest",
    "PlaceSearchResult",
    "PlaceSearchResultMixin",
    "PlaceSupplier",
    "PlaceUser",
    "VisibilityStr",
]
