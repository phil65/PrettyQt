"""Tests for `prettyqt` package."""

# import pytest

from prettyqt import core, qthelp


# from prettyqt.utils import InvalidParamError


def test_helplink():
    link = qthelp.HelpLink()
    link.get_url()


# def test_helpcontentitem():
#     item = qthelp.HelpContentItem()
#     item.get_url()
#     assert len(item) == 0


def test_helpfilterdata():
    data = qthelp.HelpFilterData()
    versions = [core.VersionNumber(1, 0, 0)]
    data.set_versions(versions)
    assert data.get_versions() == versions


# def test_helpsearchresultwidget():
#     widget = qthelp.HelpSearchResultWidget()
#     widget.get_link_at(core.Point(1, 1))


# def test_helpsearchquerywidget():
#     widget = qthelp.HelpSearchQueryWidget()
#     widget.get_link_at(core.Point(1, 1))


# def test_helpfilterengine():
#     engine = qthelp.HelpFilterEngine()
#     engine.get_available_versions()


def test_helpengine():
    engine = qthelp.HelpEngine("")
    engine.get_file_data(core.Url(""))
    engine.get_files("", "")


def test_helpsearchengine():
    core = qthelp.HelpEngineCore("")
    engine = qthelp.HelpSearchEngine(core)
    engine.search_results(0, 0)


def test_helpsearchresult():
    result = qthelp.HelpSearchResult(core.Url(""), "", "")
    result.get_url()
