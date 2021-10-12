"""Tests for `prettyqt` package."""

from prettyqt import webenginewidgets


# def test_webenginecontextmenudata(qapp):
#     page = webenginecore.WebEnginePage()
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


def test_webengineview(qapp):
    widget = webenginewidgets.WebEngineView()
    widget.set_zoom(1.5)
    widget.set_url("http://www.google.de")
    widget.load_url("http://www.google.de")
    widget.find_text("test", backward=True, case_sensitive=True, callback=None)
