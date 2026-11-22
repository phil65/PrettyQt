"""Tests for `prettyqt` package."""

import pytest


scxml = pytest.importorskip("prettyqt.scxml")


def test_scxmlcompiler(qtbot):
    from prettyqt.qt import QtCore

    reader = QtCore.QXmlStreamReader()
    compiler = scxml.ScxmlCompiler(reader)
    compiler.get_file_name()


def test_scxmlstatemachine(qtbot):
    machine = scxml.ScxmlStateMachine(scxml.QScxmlStateMachine.staticMetaObject)
    assert machine
