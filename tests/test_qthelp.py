"""Tests for `prettyqt` package."""

import sys

import pytest

import prettyqt
from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


# from prettyqt.utils import InvalidParamError


def test_helplink():
    qtlink = QtHelp.QHelpLink()
    link = qthelp.HelpLink(qtlink)
    link.get_url()


def test_helpcontentitem():
    engine = qthelp.HelpEngine("")
    model = engine.get_content_model()
    repr(model)
    # item = model.get_content_item_at(QtCore.QModelIndex())
    # item.get_url()
    # assert len(item) == 0


def test_helpcontentmodel():
    engine = qthelp.HelpEngine("")
    model = engine.get_content_model()
    repr(model)
    # model.get_content_item_at(QtCore.QModelIndex())


def test_helpfilterdata():
    data = qthelp.HelpFilterData(QtHelp.QHelpFilterData())
    versions = [core.VersionNumber(1, 0, 0)]
    data.set_versions(versions)
    assert data.get_versions() == versions


def test_helpsearchresultwidget():
    core_engine = qthelp.HelpEngineCore("")
    engine = qthelp.HelpSearchEngine(core_engine)
    widget = engine.get_result_widget()
    widget.get_link_at(core.Point(1, 1))

@pytest.mark.skipif(
    sys.platform == "linux" and prettyqt.qt.API.startswith("pyside"),
    reason="Segmentation fault",
)
def test_helpsearchquerywidget():
    widget = qthelp.HelpSearchQueryWidget()
    assert widget is not None


def test_helpfilterengine():
    core_engine = qthelp.HelpEngineCore("")
    engine = core_engine.get_filter_engine()
    engine.get_available_versions()


def test_helpengine():
    engine = qthelp.HelpEngine("")
    engine.get_file_data(core.Url(""))
    engine.get_files("", "")


def test_helpsearchengine():
    core_engine = qthelp.HelpEngineCore("")
    engine = qthelp.HelpSearchEngine(core_engine)
    engine.search_results(0, 0)


def test_helpsearchresult():
    result = qthelp.HelpSearchResult(core.Url(""), "", "")
    result.get_url()
