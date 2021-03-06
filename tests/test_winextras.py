"""Tests for `prettyqt` package."""

import pathlib
import sys

import pytest


winextras = pytest.importorskip("prettyqt.winextras")

pytestmark = pytest.mark.skipif(
    not hasattr(winextras, "WinJumpListCategory"), reason="Only supported in Qt5"
)


@pytest.mark.skipif(sys.platform != "win32", reason="Only supported on windows")
def test_winjumplistcategory(qapp):
    cat = winextras.WinJumpListCategory()
    assert len(cat) == 0
    assert cat.get_type() == "custom"
    cat.set_title("test")
    path = pathlib.Path.home()
    cat.add_destination(path)
    cat.add_link("test", path)


@pytest.mark.skipif(sys.platform != "win32", reason="Only supported on windows")
def test_winjumplistitem(qapp):
    item = winextras.WinJumpListItem("destination")
    item.set_title("test")
    item.set_icon("mdi.folder")
    path = pathlib.Path.home()
    item.set_file_path(path)
    assert item.get_file_path() == path
    item.set_working_directory(path)
    assert item.get_working_directory() == path
    item.set_type("destination")
    assert item.get_type() == "destination"


@pytest.mark.skipif(sys.platform != "win32", reason="Only supported on windows")
def test_winjumplist(qapp):
    jumplist = winextras.WinJumpList()
    jumplist.get_recent()
    jumplist.get_frequent()
    jumplist.get_tasks()
    # TODO: breaks PySide2 testing
    # jumplist.add_category("Test")
