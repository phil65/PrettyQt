"""Tests for `prettyqt` package."""

import pytest


svgwidgets = pytest.importorskip("prettyqt.svgwidgets")


def test_svgwidget(qapp):
    widget = svgwidgets.SvgWidget()
    widget.load_file("")


def test_svggraphicsitem(qapp):
    item = svgwidgets.GraphicsSvgItem()
    assert item is not None
