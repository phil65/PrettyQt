"""Tests for `prettyqt` package."""

from prettyqt import svgwidgets


# def test_svgwidget():
#     widget = svgwidgets.SvgWidget()
#     widget.load_file("")


def test_svggraphicsitem():
    item = svgwidgets.GraphicsSvgItem()
    assert item
