"""Tests for `prettyqt` package."""

import pytest

from prettyqt import openglwidgets
from prettyqt.utils import InvalidParamError


def test_openglwidget(qtbot):
    widget = openglwidgets.OpenGLWidget()
    widget.set_update_behavior("partial")
    assert widget.get_update_behavior() == "partial"
    with pytest.raises(InvalidParamError):
        widget.set_update_behavior("test")
    assert widget.get_current_target_buffer() in ("left_buffer", "right_buffer")
