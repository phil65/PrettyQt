"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, positioning
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


def test_geoaddress():
    address = positioning.GeoAddress()
    address.setCity("Test")
    assert str(address) == "Test"


def test_geolocation():
    location = positioning.GeoLocation()
    location.get_address()
    location.get_coordinate()
    location.get_bounding_shape()


def test_geocoordinate():
    coord = positioning.GeoCoordinate(11, 11)
    assert f"{coord}" == str(coord)
    assert f"{coord:default}"
    assert repr(coord) == "GeoCoordinate(11.0, 11.0)"
    assert coord.get_type() == "2d"
    assert bool(coord)


def test_geocircle():
    coord = positioning.GeoCoordinate(1, 1)
    circle = positioning.GeoCircle(coord, 0.5)
    print(str(circle))
    assert circle.get_center() == coord
    assert repr(circle) == "GeoCircle(GeoCoordinate(1.0, 1.0), 0.5)"
    assert positioning.GeoCircle(circle).get_center() == coord
    assert positioning.GeoCircle((1, 1), 0.5).get_center() == coord


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
    assert repr(path) == "GeoPath(<2 points>)"
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
    assert repr(path) == "GeoPolygon(<2 points>)"
    del path[1]
    assert len(path) == 1
    str(path)


def test_geopositioninfo():
    info = positioning.GeoPositionInfo()
    info["direction"] = 10.0
    assert "direction" in info
    assert "nonexistent" not in info
    assert info["direction"] == 10.0  # noqa: PLR2004
    info["direction_accuracy"] = 2.5
    assert "direction_accuracy" in info
    assert info["direction_accuracy"] == 2.5  # noqa: PLR2004
    del info["direction"]
    assert not bool(info)
    info.get_coordinate()
    info.get_timestamp()


def test_geosatelliteinfo():
    info = positioning.GeoSatelliteInfo()
    info["elevation"] = 1.0
    assert info["elevation"] == 1.0
    assert "elevation" in info
    assert "nonexistent" not in info
    info.setSatelliteIdentifier(1)
    assert int(info) == 1
    for system in (
        "gps",
        "glonass",
        "galileo",
        "beidou",
        "qzss",
        "irnss",
        "sbas",
        "multiple",
        "custom",
    ):
        info.set_satellite_system(system)
        assert info.get_satellite_system() == system
    with pytest.raises(InvalidParamError):
        info.set_satellite_system("test")
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
    source_no_parent = positioning.NmeaPositionInfoSource("simulation")
    assert source_no_parent.get_update_mode() == "simulation"
    with pytest.raises(InvalidParamError):
        positioning.NmeaPositionInfoSource("invalid")  # type: ignore[arg-type]
    obj = QtCore.QObject()
    source = positioning.NmeaPositionInfoSource("real_time", obj)
    print(repr(source))
    assert source.get_update_mode() == "real_time"
    assert source.get_error() == "unknown_source"
    assert "update_timeout" in positioning.geopositioninfosource.ERRORS
    assert "update_timeout" in positioning.geosatelliteinfosource.ERROR
    source.set_preferred_positioning_methods("satellite")
    # PySide6 6.12 on Windows / Python 3.15 aliases AllPositioningMethods to
    # SatellitePositioningMethods, so "all" is dropped from the mapping there.
    from prettyqt.positioning.geopositioninfosource import POSITIONING_METHODS

    expected = ["satellite", "all"] if "all" in POSITIONING_METHODS else ["satellite"]
    assert source.get_preferred_positioning_methods() == expected
    with pytest.raises(InvalidParamError):
        source.set_preferred_positioning_methods("test")
    source.get_supported_positioning_methods()
    circle = positioning.GeoCircle(positioning.GeoCoordinate(1, 1), 1.0)
    assert circle.get_type() == "circle"
