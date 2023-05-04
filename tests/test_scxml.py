"""Tests for `prettyqt` package."""

import pytest


scxml = pytest.importorskip("prettyqt.scxml")


def test_scxmlcompiler(qtbot):
    compiler = scxml.ScxmlCompiler()
    compiler.get_file_path()


def test_scxmlstatemachine(qtbot):
    machine = scxml.ScxmlStateMachine()
    assert machine
