from typing import List, Literal
import contextlib

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError, colors

CURSOR_SHAPE = bidict(
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

CursorShapeStr = Literal[
    "arrow",
    "uparrow",
    "cross",
    "wait",
    "caret",
    "size_vertical",
    "size_horizonal",
    "size_topright",
    "size_topleft",
    "size_all",
    "blank",
    "split_vertical",
    "split_horizontal",
    "pointing_hand",
    "forbidden",
    "open_hand",
    "closed_hand",
    "whats_this",
    "busy",
    "drag_move",
    "drag_copy",
    "drag_link",
    "bitmap",
]

LAYOUT_DIRECTION = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
)

LayoutDirectionStr = Literal["left_to_right", "right_to_left", "auto"]

APPLICATION_STATES = bidict(
    suspended=QtCore.Qt.ApplicationSuspended,
    hidden=QtCore.Qt.ApplicationHidden,
    inactive=QtCore.Qt.ApplicationInactive,
    active=QtCore.Qt.ApplicationActive,
)

ApplicationStateStr = Literal["suspended", "hidden", "inactive", "active"]


HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY = bidict(
    round=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round,
    ceil=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Ceil,
    floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Floor,
    round_prefer_floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor,
    pass_through=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
)

HighDpiScaleFactorRoundingPolicyStr = Literal[
    "round", "ceil", "floor", "round_prefer_floor", "pass_through"
]

QtGui.QGuiApplication.__bases__ = (core.CoreApplication,)


class GuiApplication(QtGui.QGuiApplication):
    @classmethod
    @contextlib.contextmanager
    def override_cursor(cls, cursor: CursorShapeStr):
        cls.set_override_cursor(cursor)
        yield cursor
        cls.restore_override_cursor()

    @classmethod
    def set_override_cursor(cls, cursor: CursorShapeStr):
        cursor = gui.Cursor(CURSOR_SHAPE[cursor])
        cls.setOverrideCursor(cursor)

    @classmethod
    def restore_override_cursor(cls):
        cls.restoreOverrideCursor()

    @classmethod
    def get_clipboard(cls) -> gui.Clipboard:
        return gui.Clipboard(cls.clipboard())

    def set_layout_direction(self, direction: LayoutDirectionStr):
        """Set layout direction.

        Args:
            direction: layout direction

        Raises:
            InvalidParamError: layout direction does not exist
        """
        if direction not in LAYOUT_DIRECTION:
            raise InvalidParamError(direction, LAYOUT_DIRECTION)
        self.setLayoutDirection(LAYOUT_DIRECTION[direction])

    def get_layout_direction(self) -> LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return LAYOUT_DIRECTION.inverse[self.layoutDirection()]

    @classmethod
    def set_high_dpi_scale_factor_rounding_policy(
        cls, policy: HighDpiScaleFactorRoundingPolicyStr
    ):
        """Set high dpi scale factor rounding policy.

        Args:
            direction: rounding policy

        Raises:
            InvalidParamError: rounding policy does not exist
        """
        if policy not in HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY:
            raise InvalidParamError(policy, HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY)
        cls.setHighDpiScaleFactorRoundingPolicy(
            HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY[policy]
        )

    @classmethod
    def get_high_dpi_scale_factor_rounding_policy(
        cls,
    ) -> HighDpiScaleFactorRoundingPolicyStr:
        """Get the current high dpi scale factor rounding policy.

        Returns:
            rounding policy
        """
        return HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY.inverse[
            cls.highDpiScaleFactorRoundingPolicy()
        ]

    @classmethod
    def get_application_state(cls) -> List[ApplicationStateStr]:
        """Get the current application state.

        Returns:
            application state
        """
        return [k for k, v in APPLICATION_STATES.items() if v & cls.applicationState()]

    def get_primary_screen(self) -> gui.Screen:
        return gui.Screen(self.primaryScreen())

    def get_screen_at(self, point: QtCore.QPoint) -> gui.Screen:
        return gui.Screen(self.screenAt(point))

    def get_screens(self) -> List[gui.Screen]:
        return [gui.Screen(i) for i in self.screens()]

    @classmethod
    def get_input_method(cls) -> gui.InputMethod:
        return gui.InputMethod(cls.inputMethod())

    @classmethod
    def copy_to_clipboard(cls, text: str):
        """Sets clipboard to supplied text."""
        cb = cls.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    @classmethod
    def get_font(cls) -> gui.Font:
        return gui.Font(cls.font())

    def set_icon(self, icon: gui.icon.IconType):
        """Set the default window icon.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.windowIcon())

    @classmethod
    def get_palette(cls) -> gui.Palette:
        return gui.Palette(cls.palette())
