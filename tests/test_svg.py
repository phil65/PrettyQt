"""Tests for `prettyqt` package."""

import pytest


svg = pytest.importorskip("prettyqt.svg")


def test_svggenerator():
    gen = svg.SvgGenerator()
    gen.get_size()
    gen.get_viewbox()
    gen.get_viewboxf()
