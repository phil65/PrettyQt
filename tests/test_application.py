"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError


def test_application(qapp):
    assert qapp.get_mainwindow() is None
    wnd = widgets.MainWindow()
    mw_widget = widgets.Widget()
    mw_widget.set_id("test")
    wnd.setCentralWidget(mw_widget)
    assert qapp.get_mainwindow() == wnd
    widget = qapp.get_widget(name="test")
    assert widget == mw_widget
    widget = widgets.Application["test"]
    assert widget == mw_widget
    with pytest.raises(InvalidParamError):
        qapp.get_style_icon("testus")
    icon = qapp.get_style_icon("warning")
    assert isinstance(icon, QtGui.QIcon)
    qapp.set_effect_enabled("animate_toolbox")
    with pytest.raises(InvalidParamError):
        qapp.set_effect_enabled("test")
    # assert qapp.is_effect_enabled("animate_toolbox")
    # qapp.set_navigation_mode("keypad_directional")
    # with pytest.raises(InvalidParamError):
    #     qapp.set_navigation_mode("test")
    # assert qapp.get_navigation_mode("keypad_directional")
    for widget in qapp:
        pass
    qapp.setApplicationName("testus")
    settings = core.Settings("test", "test2")
    qapp.store_widget_states(settings)
    qapp.restore_widget_states(settings)
    event = QtGui.QKeyEvent(
        QtCore.QEvent.Type.KeyPress, QtCore.Qt.Key.Key_Down, QtCore.Qt.KeyboardModifier(0)
    )
    assert qapp.send_event("test", event) is True
    qapp.post_event("test", event)
    with qapp.edit_stylesheet():
        pass


def test_guiapplication(qapp):
    qapp.set_layout_direction("right_to_left")
    with pytest.raises(InvalidParamError):
        qapp.set_layout_direction("test")
    assert qapp.get_layout_direction() == "right_to_left"
    qapp.get_font()
    qapp.get_icon()
    qapp.get_primary_screen()
    qapp.get_screens()
    qapp.get_screen_at(core.Point(1, 1))
    assert qapp.get_application_state() in [["inactive"], ["active"]]
    qapp.copy_to_clipboard("test")
    qapp.set_icon("mdi.timer")
    qapp.set_icon(None)
    qapp.set_high_dpi_scale_factor_rounding_policy("round_prefer_floor")
    with pytest.raises(InvalidParamError):
        qapp.set_high_dpi_scale_factor_rounding_policy("testus")
    assert qapp.get_high_dpi_scale_factor_rounding_policy() == "round_prefer_floor"


def test_coreapplication(qapp):
    qapp.get_application_file_path()
    expected = core.Dir.toNativeSeparators(qapp.applicationFilePath())
    assert str(qapp.get_application_file_path()) == expected
    qapp.get_application_dir_path()
    qapp.add_library_path("")
    qapp.get_library_paths()
    qapp.disable_window_help_button()
    qapp.set_metadata(
        app_name="test", app_version="1.0.0", org_name="test", org_domain="test"
    )
    qapp.load_language("de")
    qapp.removeTranslator(qapp.translators["de"])
