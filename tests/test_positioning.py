#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from qtpy import QtCore

from prettyqt import core, positioning
from prettyqt.utils import InvalidParamError


def test_geoaddress():
    address = positioning.GeoAddress()
    address.setCity("Test")
    assert str(address) == "Test"


def test_geolocation():
    location = positioning.GeoLocation()
    location.get_address()
    location.get_coordinate()
    location.get_bounding_box()


def test_geocoordinate():
    coord = positioning.GeoCoordinate(11, 11)
    print(str(coord))
    assert repr(coord) == "GeoCoordinate(11.0, 11.0)"
    assert coord.get_type() == "two_d"
    assert bool(coord) is True


def test_geocircle():
    coord = positioning.GeoCoordinate(1, 1)
    circle = positioning.GeoCircle(coord, 0.5)
    print(str(circle))
    assert circle.get_center() == coord
    assert repr(circle) == "GeoCircle(GeoCoordinate(1.0, 1.0), 0.5)"


def test_georectangle():
    coord1 = positioning.GeoCoordinate(1, 1)
    coord2 = positioning.GeoCoordinate(5, 5)
    rect = positioning.GeoRectangle(coord1, coord2)
    assert repr(rect) == "GeoRectangle(GeoCoordinate(1.0, 1.0), GeoCoordinate(5.0, 5.0))"


def test_geopath():
    coord1 = positioning.GeoCoordinate(1, 1)
    coord2 = positioning.GeoCoordinate(5, 5)
    path = positioning.GeoPath()
    path += coord1
    path += coord2
    path[1] = coord2
    assert path[1] == coord2
    assert repr(path) == "GeoPath(GeoCoordinate(1.0, 1.0), GeoCoordinate(5.0, 5.0))"
    assert positioning.GeoCoordinate(1, 1) in path
    del path[1]
    assert len(path) == 1


def test_geopolygon():
    coord1 = positioning.GeoCoordinate(1, 1)
    coord2 = positioning.GeoCoordinate(5, 5)
    path = positioning.GeoPolygon()
    path += coord1
    path += coord2
    path[1] = coord2
    assert path[1] == coord2
    assert repr(path) == "GeoPolygon(GeoCoordinate(1.0, 1.0), GeoCoordinate(5.0, 5.0))"
    del path[1]
    assert len(path) == 1
    str(path)


def test_geosatelliteinfo():
    info = positioning.GeoSatelliteInfo()
    info["elevation"] = 1.0
    assert info["elevation"] == 1.0
    assert "elevation" in info
    info.setSatelliteIdentifier(1)
    assert int(info) == 1
    info.set_satellite_system("gps")
    with pytest.raises(InvalidParamError):
        info.set_satellite_system("test")
    assert info.get_satellite_system() == "gps"
    del info["elevation"]


def test_geoareamonitorsource():
    obj = core.Object()
    source = positioning.GeoAreaMonitorSource(obj)
    str(source)
    # assert source.get_error() == "none"


def test_geoareamonitorinfo():
    info = positioning.GeoAreaMonitorInfo()
    str(info)
    info.get_expiration()
    info.get_area()


def test_nmeapositioninfosource():
    obj = QtCore.QObject()
    source = positioning.NmeaPositionInfoSource("real_time", obj)
    print(repr(source))
    assert source.get_update_mode() == "real_time"
    assert source.get_error() == "unknown_source"
    source.set_preferred_positioning_methods("satellite")
    assert source.get_preferred_positioning_methods() == ["satellite", "all"]
    with pytest.raises(InvalidParamError):
        source.set_preferred_positioning_methods("test")
    source.get_supported_positioning_methods()
