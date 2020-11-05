#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""
import pytest

from prettyqt import network, core
from prettyqt.utils import InvalidParamError


def test_httppart():
    part = network.HttpPart()
    part.set_body("test")
    part.set_headers(dict(a="b"))
    part.set_header("location", "c")


def test_httpmultipart():
    part = network.HttpMultiPart()
    part.set_content_type("related")
    with pytest.raises(InvalidParamError):
        part.set_content_type("test")
    part.set_boundary("test")
    assert part.get_boundary() == "test"


def test_networkrequest():
    req = network.NetworkRequest()
    headers = {"a": "b"}
    req.set_headers(headers)
    assert req.get_headers() == headers
    req.set_priority("low")
    assert req.get_priority() == "low"
    req.set_url("http://www.google.de")
    assert req.get_url() == core.Url("http://www.google.de")
    with pytest.raises(InvalidParamError):
        req.set_header("test", "test")
    req.set_header("location", "test")
    with pytest.raises(InvalidParamError):
        req.get_header("test")
    assert req.get_header("location") == "test"


def test_networkaccessmanager():
    manager = network.NetworkAccessManager()
    manager.set_redirect_policy("no_less_safe")
    with pytest.raises(InvalidParamError):
        manager.set_redirect_policy("test")
    assert manager.get_redirect_policy() == "no_less_safe"


def test_networkcookie():
    cookie = network.NetworkCookie()
    cookie.set_name("test")
    assert cookie.get_name() == "test"
    cookie.set_value("testus")
    assert cookie.get_value() == "testus"
    assert cookie.to_raw_form(full=False) is None


def test_networkcookiejar():
    jar = network.NetworkCookieJar()
    assert jar["test"] == []
    for i in jar:
        pass
    repr(jar)
