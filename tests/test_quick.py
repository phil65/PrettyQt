"""Tests for `prettyqt` package."""


import pathlib

import pytest

from prettyqt import core, gui, quick
from prettyqt.utils import InvalidParamError


def test_quickitem():
    item = quick.QuickItem()
    item.get_children_rect()
    item.get_cursor()
    item.get_flags()
    item.set_transform_origin("bottom")
    with pytest.raises(InvalidParamError):
        item.set_transform_origin("test")
    assert item.get_transform_origin() == "bottom"


def test_quickpainteditem():
    item = quick.QuickPaintedItem()
    item.get_fill_color()
    item.get_texture_size()
    item.set_render_target("framebuffer_object")
    with pytest.raises(InvalidParamError):
        item.set_render_target("test")
    assert item.get_render_target() == "framebuffer_object"


def test_quickview():
    view = quick.QuickView()
    path = pathlib.Path.cwd() / "tests" / "qmltest.qml"
    view.set_source(path)
    assert view.get_source() == path
    assert view.get_status() == "ready"


def test_quickwindow():
    window = quick.QuickWindow()
    window.create_texture_from_image(gui.Image())
    window.grab_window()
    window.get_color()
    window.get_render_target_size()
    window.set_text_render_type("native_text")
    with pytest.raises(InvalidParamError):
        window.set_text_render_type("test")
    assert window.get_text_render_type() == "native_text"
    with window.external_commands():
        pass
    runnable = core.Runnable()
    with pytest.raises(InvalidParamError):
        window.schedule_render_job(runnable, "test")
    window.schedule_render_job(runnable, "before_rendering")
