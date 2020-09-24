#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

from prettyqt import network, core


def test_networkrequest():
    req = network.NetworkRequest()
    headers = {"a": "b"}
    req.set_headers(headers)
    assert req.get_headers() == headers
    req.set_priority("low")
    assert req.get_priority() == "low"
    req.set_url("http://www.google.de")
    assert req.get_url() == core.Url("http://www.google.de")


def test_networkaccessmanager():
    manager = network.NetworkAccessManager()
    manager.set_redirect_policy("no_less_safe")
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
