"""Tests for `prettyqt` package."""

from prettyqt import openglwidgets


def test_openglwidget(qtbot):
    openglwidgets.OpenGLWidget()
