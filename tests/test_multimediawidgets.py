"""Tests for `prettyqt` package."""

import pytest

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError


multimediawidgets = pytest.importorskip("prettyqt.multimediawidgets")


def test_videowidget(qapp):
    widget = multimediawidgets.VideoWidget()
    widget.set_doubleclick_for_fullscreen(True)
    event = gui.QMouseEvent(
        core.QEvent.Type.MouseButtonDblClick,
        core.QPointF(0, 0),
        core.QPointF(0, 0),
        constants.MouseButton.LeftButton,
        constants.MouseButton.LeftButton,
        constants.KeyboardModifier.NoModifier,
    )
    widget.mouseDoubleClickEvent(event)
    assert event.isAccepted()


def test_graphicsvideoitem(qapp):
    item = multimediawidgets.GraphicsVideoItem()
    item.get_offset()
    item.get_native_size()
    item.get_size()
    item.set_aspect_ratio_mode("keep")
    with pytest.raises(InvalidParamError):
        item.set_aspect_ratio_mode("test")
    assert item.get_aspect_ratio_mode() == "keep"
