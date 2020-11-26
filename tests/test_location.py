#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from qtpy import QtLocation

from prettyqt import location, core
from prettyqt.utils import InvalidParamError


def test_geocodingmanager(qtlog):
    with qtlog.disabled():
        provider = location.GeoServiceProvider("osm")
        manager = provider.get_geocoding_manager()
    manager.get_locale()


def test_georoutingmanager():
    provider = location.GeoServiceProvider("osm")
    manager = provider.get_routing_manager()
    manager.get_locale()
    manager.get_supported_feature_types()
    manager.get_supported_feature_weights()
    manager.get_supported_maneuver_details()
    manager.get_supported_route_optimizations()
    manager.get_supported_segment_details()
    manager.get_supported_travel_modes()


def test_geomaneuver():
    maneuver = location.GeoManeuver()
    maneuver["test"] = "a"
    assert maneuver["test"] == "a"
    assert str(maneuver) == ""
    assert bool(maneuver) is True
    maneuver.get_position()
    assert maneuver.get_waypoint() is None
    maneuver.set_direction("hard_left")
    assert maneuver.get_direction() == "hard_left"


def test_georoute():
    route = location.GeoRoute()
    route["test"] = "a"
    assert route["test"] == "a"
    abs(route) == 0
    route.get_bounds()
    route.get_first_route_segment()
    route.get_path()


def test_georouteleg():
    location.GeoRouteLeg()


def test_georouterequest():
    request = location.GeoRouteRequest()
    request.get_waypoints()
    request.get_exclude_areas()
    request.get_departure_time()
    request.set_feature_weight("public_transit", "require")
    with pytest.raises(InvalidParamError):
        request.set_feature_weight("public_transit", "test")
    with pytest.raises(InvalidParamError):
        request.set_feature_weight("test", "require")
    assert request.get_feature_weight("public_transit") == "require"
    request.set_route_optimization("most_economic")
    with pytest.raises(InvalidParamError):
        request.set_route_optimization("test")
    assert request.get_route_optimization() == "most_economic"
    request.set_travel_modes("car")
    assert request.get_travel_modes() == ["car"]
    request.get_feature_types()


def test_georoutesegment():
    segment = location.GeoRouteSegment()
    assert bool(segment) is False
    assert abs(segment) == 0
    segment.get_maneuver()
    segment.get_path()


def test_geoserviceprovider():
    provider = location.GeoServiceProvider("osm")
    assert provider.get_error() == "none"
    assert provider.get_geocoding_error() == "none"
    assert provider.get_geocoding_features() == ["online", "reverse"]
    assert provider.get_mapping_error() == "none"
    assert provider.get_mapping_features() == ["online"]
    assert provider.get_navigation_error() == "none"
    assert provider.get_navigation_features() == []
    assert provider.get_places_error() == "none"
    assert provider.get_places_features() == ["online_places"]
    assert provider.get_routing_error() == "none"
    assert provider.get_routing_features() == ["online"]


def test_placeattribute():
    attr = location.PlaceAttribute()
    assert bool(attr) is False
    attr.setLabel("Test")
    attr.setText("Text")
    assert str(attr) == "Test: Text"


def test_placecategory():
    cat = location.PlaceCategory()
    cat.get_icon()
    assert cat.get_visibility() == "unspecified"
    assert bool(cat) is False
    assert str(cat) == ""


def test_placecontactdetail():
    detail = location.PlaceContactDetail()
    detail.setLabel("Label")
    detail.setValue("Value")
    assert str(detail) == "Label: Value"


def test_placeicon():
    icon = location.PlaceIcon()
    assert bool(icon) is False
    icon["test"] = True
    assert icon["test"] is True
    # icon.get_manager()
    icon.get_url()


def test_placemanager():
    provider = location.GeoServiceProvider("osm")
    manager = provider.get_place_manager()
    manager.get_locales()
    manager.get_category("test")
    manager.get_child_categories("test")


def test_placeuser():
    user = location.PlaceUser()
    assert str(user) == ""


def test_placeimage():
    image = location.PlaceImage()
    image.get_supplier()
    assert str(image) == ""
    image.set_url("http://")
    assert image.get_url() == core.Url("http://")


def test_placereview():
    review = location.PlaceReview()
    review.get_datetime()
    str(review)


def test_placereply():
    reply = location.PlaceReply()
    assert reply.get_error() == "none"
    assert reply.get_type() == "generic"


def test_placesearchreply():
    reply = location.PlaceSearchReply()
    for result in reply:
        pass
    assert len(reply) == 0
    assert len(reply.get_results()) == 0
    with pytest.raises(IndexError):
        reply[0]
    reply.get_previous_page_request()
    reply.get_next_page_request()
    reply.get_request()
    obj = QtLocation.QPlaceSearchReply()
    location.PlaceSearchReply.clone_from(obj)


def test_placecontentreply():
    reply = location.PlaceContentReply()
    assert len(reply) == 0
    reply.get_previous_page_request()
    reply.get_next_page_request()
    reply.get_request()
    obj = QtLocation.QPlaceContentReply()
    location.PlaceContentReply.clone_from(obj)


def test_placedetailsreply():
    reply = location.PlaceDetailsReply()
    reply.get_place()
    obj = QtLocation.QPlaceDetailsReply()
    location.PlaceDetailsReply.clone_from(obj)


def test_placeidreply():
    reply = location.PlaceIdReply(0)
    assert reply.get_operation_type() == "save_place"
    obj = QtLocation.QPlaceIdReply(0)
    location.PlaceIdReply.clone_from(obj)


def test_placematchreply():
    reply = location.PlaceMatchReply()
    for result in reply:
        pass
    assert len(reply) == 0
    assert len(reply.get_places()) == 0
    with pytest.raises(IndexError):
        reply[0]
    reply.get_request()
    obj = QtLocation.QPlaceMatchReply()
    location.PlaceMatchReply.clone_from(obj)


def test_placesearchresult():
    result = location.PlaceSearchResult()
    result.get_icon()
    assert result.get_type() == "unknown"


def test_placeresult():
    result = location.PlaceResult()
    result.get_place()


def test_placeeditorial():
    editorial = location.PlaceEditorial()
    str(editorial)


def test_placesupplier():
    supplier = location.PlaceSupplier()
    supplier.set_url("http://")
    assert supplier.get_url() == core.Url("http://")
    supplier.get_icon()
    assert bool(supplier) is True


def test_placeratings():
    ratings = location.PlaceRatings()
    ratings.setAverage(1.5)
    assert float(ratings) == 1.5
    assert bool(ratings) is True


def test_place():
    place = location.Place()
    place.get_categories()
    place.get_contact_details("email")
    content = location.PlaceEditorial()
    collection = {0: content}
    place.set_content("image", collection)
    assert place.get_content("image") == collection
    place.get_icon()
    place.get_location()
    place.get_primary_website()
    place.get_ratings()
    place.get_supplier()
    assert place.get_visibility() == "unspecified"


def test_placesearchrequest():
    request = location.PlaceSearchRequest()
    request.get_visibility_scope()
    request.get_categories()
    request.get_search_area()
    request.set_relevance_hint("distance")
    with pytest.raises(InvalidParamError):
        request.set_relevance_hint("test")
    assert request.get_relevance_hint() == "distance"


def test_placecontentrequest():
    request = location.PlaceContentRequest()
    request.set_content_type("image")
    with pytest.raises(InvalidParamError):
        request.set_content_type("test")
    assert request.get_content_type() == "image"


def test_placematchrequest():
    request = location.PlaceMatchRequest()
    request["test"] = "abc"
    assert request["test"] == "abc"
    request.get_places()
