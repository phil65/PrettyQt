"""Tests for `prettyqt` package."""

import warnings

import pytest

from prettyqt import core, webenginecore
from prettyqt.utils import InvalidParamError


def test_webengineurlscheme(qapp):
    scheme = webenginecore.WebEngineUrlScheme()
    scheme.set_name("test")
    assert scheme.get_name() == "test"
    scheme.set_syntax("host")
    with pytest.raises(InvalidParamError):
        scheme.set_syntax("test")
    assert scheme.get_syntax() == "host"
    assert "fetch_api_allowed" in webenginecore.webengineurlscheme.FLAGS
    assert hasattr(webenginecore, "WebEngineHistoryModel")
    assert (
        "network_failed"
        in webenginecore.webenginedownloadrequest.DOWNLOAD_INTERRUPT_REASONS
    )


def test_webenginehttprequest(qapp):
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
    profile.set_persistent_cookie_policy("only_persistent")
    assert profile.get_persistent_cookie_policy() == "only_persistent"
    profile.set_persistent_cookie_policy("force")
    with pytest.raises(InvalidParamError):
        profile.set_persistent_cookie_policy("test")
    assert profile.get_persistent_cookie_policy() == "force"
    profile.set_http_cache_type("disk")
    with pytest.raises(InvalidParamError):
        profile.set_http_cache_type("test")
    assert profile.get_http_cache_type() == "disk"
    profile.install_url_scheme_handler("custom", lambda _job: None)
    assert profile.urlSchemeHandler(b"custom") is not None
    profile.get_scripts()


def test_webenginescript(qapp):
    script = webenginecore.WebEngineScript()
    script.set_injection_point("document_ready")
    with pytest.raises(InvalidParamError):
        script.set_injection_point("test")
    assert script.get_injection_point() == "document_ready"


def test_webenginescriptcollection(qapp):
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
    with pytest.raises(KeyError):
        _ = item["nonexistent"]


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
    with pytest.raises(InvalidParamError):
        settings.get_font_family("test")
    assert settings.get_font_family("sans_serif") == "verdana"
    settings.set_font_size("default_fixed", 14)
    with pytest.raises(InvalidParamError):
        settings.set_font_size("test", "test")
    with pytest.raises(InvalidParamError):
        settings.get_font_size("test")
    assert settings.get_font_size("default_fixed") == 14  # noqa: PLR2004
    settings["force_dark_mode"] = True
    assert settings["force_dark_mode"] is True


def test_webenginehistory(qapp):
    page = webenginecore.WebEnginePage()
    history = page.get_history()
    assert (
        len(history) < 2  # noqa: PLR2004
    )  # 0 returns 1 for PySide6 6.5, 0 for PyQt6 6.4
    for _item in history:
        pass
    history.get_items()


def test_webenginepage(qapp, tmp_path):
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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        page.set_feature_permission(
            "http://www.google.de", "clipboard_read_write", "granted_by_user"
        )
    page.insert_stylesheet("percent_css", "body { width: 100%; }", immediately=False)
    assert "percent_css" in [s.name() for s in page.get_scripts()]
    css_file = tmp_path / "style.css"
    css_file.write_text("p { margin: 50%; }", encoding="utf-8")
    page.insert_stylesheet("file_css", css_file, immediately=False)
    assert "file_css" in [s.name() for s in page.get_scripts()]
    page.get_settings()
    page.set_setting("auto_load_images", False)
    assert page.get_setting("auto_load_images") is False
    page.get_icon_url()
    page.get_requested_url()
    page.get_scroll_position()
    page.get_contents_size()
    # page.choose_files("open", [], [])


def test_webenginepermission(qapp):
    perm = webenginecore.WebEnginePermission()
    assert not perm
    assert not perm.isValid()
    assert perm.get_origin() == core.Url()
    assert perm.get_permission_type() == "unsupported"
    assert perm.get_state() == "invalid"
    repr(perm)
    assert webenginecore.WebEnginePermission.is_persistent("notifications") is True
    assert webenginecore.WebEnginePermission.is_persistent("unsupported") is False
    with pytest.raises(InvalidParamError):
        webenginecore.WebEnginePermission.is_persistent("invalid")
    assert "geolocation" in webenginecore.webenginepermission.PERMISSION_TYPE
    assert "granted" in webenginecore.webenginepermission.STATE
