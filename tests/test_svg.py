"""Tests for `prettyqt` package."""

from prettyqt import svg


def test_svggenerator():
    gen = svg.SvgGenerator()
    gen.get_size()
    gen.get_viewbox()
    gen.get_viewboxf()
