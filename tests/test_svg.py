"""Tests for `prettyqt` package."""

import pytest

from prettyqt.utils import InvalidParamError


svg = pytest.importorskip("prettyqt.svg")


def test_svggenerator():
    gen = svg.SvgGenerator()
    gen.get_size()
    gen.get_viewbox()
    gen.get_viewboxf()


def test_svgrenderer():
    renderer = svg.SvgRenderer()
    with pytest.raises(ValueError):
        renderer.load_file("test")
    renderer.set_aspect_ratio_mode("ignore")
    assert renderer.get_aspect_ratio_mode() == "ignore"
    with pytest.raises(InvalidParamError):
        renderer.set_aspect_ratio_mode("test")
