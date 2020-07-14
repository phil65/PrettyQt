#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `prettyqt` package."""

import pathlib

from prettyqt import winextras


def test_winjumplistcategory(qapp):
    cat = winextras.WinJumpListCategory()
    assert len(cat) == 0
    assert cat.get_type() == "custom"


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


def test_winjumplist(qapp):
    jumplist = winextras.WinJumpList()
    jumplist.add_category("Test")
    jumplist.get_recent()
    jumplist.get_frequent()
    jumplist.get_tasks()
