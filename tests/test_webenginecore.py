"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, webenginecore
from prettyqt.utils import InvalidParamError


def test_webengineurlscheme():
    scheme = webenginecore.WebEngineUrlScheme()
    scheme.set_name("test")
    assert scheme.get_name() == "test"
    scheme.set_syntax("host")
    with pytest.raises(InvalidParamError):
        scheme.set_syntax("test")
    assert scheme.get_syntax() == "host"


def test_webenginehttprequest():
    req = webenginecore.WebEngineHttpRequest()
    headers = {"a": "b"}
    req.set_headers(headers)
    assert req.get_headers() == headers
    req.set_method("post")
    with pytest.raises(InvalidParamError):
        req.set_method("test")
    assert req.get_method() == "post"
    req.set_url("http://www.google.de")
    assert req.get_url() == core.Url("http://www.google.de")
    req.get_post_data()


def test_webengineprofile(qapp):
    profile = webenginecore.WebEngineProfile("MyProfile")
    profile.set_persistent_cookie_policy("force")
    with pytest.raises(InvalidParamError):
        profile.set_persistent_cookie_policy("test")
    assert profile.get_persistent_cookie_policy() == "force"
    profile.set_http_cache_type("disk")
    with pytest.raises(InvalidParamError):
        profile.set_http_cache_type("test")
    assert profile.get_http_cache_type() == "disk"
    profile.get_scripts()


def test_webenginescript():
    script = webenginecore.WebEngineScript()
    script.set_injection_point("document_ready")
    with pytest.raises(InvalidParamError):
        script.set_injection_point("test")
    assert script.get_injection_point() == "document_ready"


def test_webenginescriptcollection():
    page = webenginecore.WebEnginePage()
    script = webenginecore.WebEngineScript()
    script.setName("test")
    item = page.get_scripts()
    assert not bool(item)
    item += script
    assert script in item
    assert len(item) == 1
    assert bool(item)
    for _scr in item:
        pass
    assert item["test"] == script


def test_webenginesettings(qapp):
    page = webenginecore.WebEnginePage()
    settings = page.get_settings()
    settings["auto_load_images"] = False
    assert settings["auto_load_images"] is False
    del settings["auto_load_images"]
    settings.set_unknown_url_scheme_policy("allow_all")
    with pytest.raises(InvalidParamError):
        settings.set_unknown_url_scheme_policy("test")
    assert settings.get_unknown_url_scheme_policy() == "allow_all"
    settings.set_font_family("sans_serif", "verdana")
    with pytest.raises(InvalidParamError):
        settings.set_font_family("test", "test")
    assert settings.get_font_family("sans_serif") == "verdana"
    settings.set_font_size("default_fixed", 14)
    with pytest.raises(InvalidParamError):
        settings.set_font_size("test", "test")
    assert settings.get_font_size("default_fixed") == 14


def test_webenginehistory():
    page = webenginecore.WebEnginePage()
    history = page.get_history()
    assert len(history) < 2  # 0 returns 1 for PySide6 6.5, 0 for PyQt6 6.4
    for _item in history:
        pass
    history.get_items()


def test_webenginepage(qapp):
    page = webenginecore.WebEnginePage()
    page.set_zoom(1.5)
    page.set_url("http://www.google.de")
    assert page.get_url() == core.Url("http://www.google.de")
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
    page.get_settings()
    page.set_setting("auto_load_images", False)
    assert page.get_setting("auto_load_images") is False
    page.get_icon_url()
    page.get_requested_url()
    page.get_scroll_position()
    page.get_contents_size()
    # page.choose_files("open", [], [])
