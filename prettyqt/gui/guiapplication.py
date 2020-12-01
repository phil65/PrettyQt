# -*- coding: utf-8 -*-

from typing import List
import contextlib

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

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

LAYOUT_DIRECTIONS = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
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

    @classmethod
    def get_clipboard(cls) -> gui.Clipboard:
        return gui.Clipboard(cls.clipboard())

    def set_layout_direction(self, direction: str):
        """Set layout direction.

        Valid values: "left_to_right", "right_to_left", "auto"

        Args:
            direction: layout direction

        Raises:
            InvalidParamError: layout direction does not exist
        """
        if direction not in LAYOUT_DIRECTIONS:
            raise InvalidParamError(direction, LAYOUT_DIRECTIONS)
        self.setLayoutDirection(LAYOUT_DIRECTIONS[direction])

    def get_layout_direction(self) -> str:
        """Get the current layout direction.

        Possible values: "left_to_right", "right_to_left", "auto"

        Returns:
            layout direction
        """
        return LAYOUT_DIRECTIONS.inv[self.layoutDirection()]

    def get_primary_screen(self) -> gui.Screen:
        return gui.Screen(self.primaryScreen())

    def get_screen_at(self, point: QtCore.QPoint) -> gui.Screen:
        return gui.Screen(self.screenAt(point))

    def get_screens(self) -> List[gui.Screen]:
        return [gui.Screen(i) for i in self.screens()]

    def get_input_method(self) -> gui.InputMethod:
        return gui.InputMethod(self.inputMethod())
