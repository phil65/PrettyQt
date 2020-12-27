"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core
from prettyqt.utils import InvalidParamError


webenginewidgets = pytest.importorskip("prettyqt.webenginewidgets")


# def test_webenginecontextmenudata(qapp):
#     page = webenginewidgets.WebEnginePage()
#     data = page.get_context_menu_data()
#     data.get_media_url()
#     data.get_link_url()
#     data.get_media_flags()
#     data.get_edit_flags()
#     assert data.can_undo() is True
#     assert data.can_redo() is True
#     assert data.can_cut() is True
#     assert data.can_copy() is True
#     assert data.can_paste() is True
#     assert data.can_delete() is True
#     assert data.can_select_all() is True
#     assert data.can_translate() is True
#     assert data.can_edit_richly() is True


def test_webenginehistory():
    page = webenginewidgets.WebEnginePage()
    history = page.get_history()
    assert len(history) == 0
    for item in history:
        pass
    history.get_items()


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
    profile.get_scripts()


def test_webenginescript():
    script = webenginewidgets.WebEngineScript()
    script.set_injection_point("document_ready")
    with pytest.raises(InvalidParamError):
        script.set_injection_point("test")
    assert script.get_injection_point() == "document_ready"


def test_webenginescriptcollection():
    page = webenginewidgets.WebEnginePage()
    script = webenginewidgets.WebEngineScript()
    script.setName("test")
    item = page.get_scripts()
    assert bool(item) is False
    item += script
    assert script in item
    assert len(item) == 1
    assert bool(item) is True
    for scr in item:
        pass
    assert item["test"] == script


def test_webenginesettings(qapp):
    page = webenginewidgets.WebEnginePage()
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
