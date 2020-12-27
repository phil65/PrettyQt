"""Location module."""

import prettyqt.qt

from .qlocation import VISIBILITY, VisibilityStr
from .georouterequest import GeoRouteRequest
from .placeattribute import PlaceAttribute
from .placeratings import PlaceRatings
from .placecontactdetail import PlaceContactDetail
from .placeicon import PlaceIcon
from .placesupplier import PlaceSupplier
from .placecategory import PlaceCategory
from .placeuser import PlaceUser
from .placecontent import PlaceContent
from .placeimage import PlaceImage
from .placereview import PlaceReview
from .placeeditorial import PlaceEditorial
from .geocodingmanager import GeoCodingManager
from .georoutingmanager import GeoRoutingManager
from .geomaneuver import GeoManeuver
from .georoutesegment import GeoRouteSegment
from .georoute import GeoRoute
from .placesearchrequest import PlaceSearchRequest
from .placecontentrequest import PlaceContentRequest
from .place import Place
from .placematchrequest import PlaceMatchRequest
from .placesearchresult import PlaceSearchResult
from .placeresult import PlaceResult
from .placeproposedsearchresult import PlaceProposedSearchResult
from .placereply import PlaceReply
from .placesearchreply import PlaceSearchReply
from .placecontentreply import PlaceContentReply
from .placedetailsreply import PlaceDetailsReply
from .placematchreply import PlaceMatchReply
from .placeidreply import PlaceIdReply
from .placemanager import PlaceManager
from .geoserviceprovider import GeoServiceProvider

# not available in PySide2
if prettyqt.qt.API == "pyqt5":
    from .georouteleg import GeoRouteLeg


__all__ = [
    "VISIBILITY",
    "VisibilityStr",
    "PlaceAttribute",
    "PlaceContactDetail",
    "PlaceCategory",
    "PlaceRatings",
    "PlaceUser",
    "Place",
    "PlaceSupplier",
    "PlaceManager",
    "PlaceIcon",
    "PlaceContent",
    "PlaceImage",
    "PlaceReview",
    "PlaceEditorial",
    "GeoCodingManager",
    "GeoRoutingManager",
    "GeoManeuver",
    "GeoRoute",
    "GeoRouteLeg",
    "GeoRouteRequest",
    "GeoRouteSegment",
    "PlaceSearchRequest",
    "PlaceContentRequest",
    "PlaceMatchRequest",
    "GeoServiceProvider",
    "PlaceReply",
    "PlaceSearchReply",
    "PlaceContentReply",
    "PlaceDetailsReply",
    "PlaceMatchReply",
    "PlaceIdReply",
    "PlaceSearchResult",
    "PlaceResult",
    "PlaceProposedSearchResult",
]
