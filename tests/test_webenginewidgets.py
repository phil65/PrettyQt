#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pytest

from prettyqt import webenginewidgets
from prettyqt.utils import InvalidParamError


def test_webengineview(qapp):
    widget = webenginewidgets.WebEngineView()
    widget.set_zoom(1.5)
    widget.set_url("http://www.google.de")
    widget.load_url("http://www.google.de")
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)


def test_webenginepage(qapp):
    page = webenginewidgets.WebEnginePage()
    page.set_zoom(1.5)
    page.set_url("http://www.google.de")
    page.load_url("http://www.google.de")
    page.find_text("test", backward=True, case_sensitive=True, callback=None)
    page.set_lifecycle_state("discarded")
    with pytest.raises(InvalidParamError):
        page.set_lifecycle_state("test")
    assert page.get_lifecycle_state() == "discarded"
    page.trigger_action("select_all")
    page.set_feature_permission(
        "http://www.google.de", "media_audio_capture", "granted_by_user"
    )


def test_webengineprofile(qapp):
    profile = webenginewidgets.WebEngineProfile("MyProfile")
    profile.set_persistent_cookie_policy("force")
    with pytest.raises(InvalidParamError):
        profile.set_persistent_cookie_policy("test")
    assert profile.get_persistent_cookie_policy() == "force"
    profile.set_http_cache_type("disk")
    with pytest.raises(InvalidParamError):
        profile.set_http_cache_type("test")
    assert profile.get_http_cache_type() == "disk"


def test_webenginescript():
    script = webenginewidgets.WebEngineScript()
    script.set_injection_point("document_ready")
    with pytest.raises(InvalidParamError):
        script.set_injection_point("test")
    assert script.get_injection_point() == "document_ready"
