# -*- coding: utf-8 -*-
"""
"""

import contextlib

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict

CURSOR_SHAPES = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    uparrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
    size_vertical=QtCore.Qt.SizeVerCursor,
    size_horizonal=QtCore.Qt.SizeHorCursor,
    size_topright=QtCore.Qt.SizeBDiagCursor,
    size_topleft=QtCore.Qt.SizeFDiagCursor,
    size_all=QtCore.Qt.SizeAllCursor,
    blank=QtCore.Qt.BlankCursor,
    split_vertical=QtCore.Qt.SplitVCursor,
    split_horizontal=QtCore.Qt.SplitHCursor,
    pointing_hand=QtCore.Qt.PointingHandCursor,
    forbidden=QtCore.Qt.ForbiddenCursor,
    open_hand=QtCore.Qt.OpenHandCursor,
    closed_hand=QtCore.Qt.ClosedHandCursor,
    whats_this=QtCore.Qt.WhatsThisCursor,
    busy=QtCore.Qt.BusyCursor,
    drag_move=QtCore.Qt.DragMoveCursor,
    drag_copy=QtCore.Qt.DragCopyCursor,
    drag_link=QtCore.Qt.DragLinkCursor,
    bitmap=QtCore.Qt.BitmapCursor,
)


QtGui.QGuiApplication.__bases__ = (core.CoreApplication,)


class GuiApplication(QtGui.QGuiApplication):
    @classmethod
    @contextlib.contextmanager
    def override_cursor(cls, cursor: str):
        cls.set_override_cursor(cursor)
        yield cursor
        cls.restore_override_cursor()

    @classmethod
    def set_override_cursor(cls, cursor: str):
        cursor = gui.Cursor(CURSOR_SHAPES[cursor])
        cls.setOverrideCursor(cursor)

    @classmethod
    def restore_override_cursor(cls):
        cls.restoreOverrideCursor()
