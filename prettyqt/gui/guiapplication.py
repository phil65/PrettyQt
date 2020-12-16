import contextlib
from typing import List

from qtpy import QtCore, QtGui

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError, colors


QtGui.QGuiApplication.__bases__ = (core.CoreApplication,)


class GuiApplication(QtGui.QGuiApplication):
    @classmethod
    @contextlib.contextmanager
    def override_cursor(cls, cursor: constants.CursorShapeStr):
        cls.set_override_cursor(cursor)
        yield cursor
        cls.restore_override_cursor()

    @classmethod
    def set_override_cursor(cls, cursor: constants.CursorShapeStr):
        cursor = gui.Cursor(constants.CURSOR_SHAPE[cursor])
        cls.setOverrideCursor(cursor)

    @classmethod
    def restore_override_cursor(cls):
        cls.restoreOverrideCursor()

    @classmethod
    def get_clipboard(cls) -> gui.Clipboard:
        return gui.Clipboard(cls.clipboard())

    def set_layout_direction(self, direction: constants.LayoutDirectionStr):
        """Set layout direction.

        Args:
            direction: layout direction

        Raises:
            InvalidParamError: layout direction does not exist
        """
        if direction not in constants.LAYOUT_DIRECTION:
            raise InvalidParamError(direction, constants.LAYOUT_DIRECTION)
        self.setLayoutDirection(constants.LAYOUT_DIRECTION[direction])

    def get_layout_direction(self) -> constants.LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return constants.LAYOUT_DIRECTION.inverse[self.layoutDirection()]

    @classmethod
    def set_high_dpi_scale_factor_rounding_policy(
        cls, policy: constants.HighDpiScaleFactorRoundingPolicyStr
    ):
        """Set high dpi scale factor rounding policy.

        Args:
            direction: rounding policy

        Raises:
            InvalidParamError: rounding policy does not exist
        """
        if policy not in constants.HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY:
            raise InvalidParamError(
                policy, constants.HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY
            )
        cls.setHighDpiScaleFactorRoundingPolicy(
            constants.HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY[policy]
        )

    @classmethod
    def get_high_dpi_scale_factor_rounding_policy(
        cls,
    ) -> constants.HighDpiScaleFactorRoundingPolicyStr:
        """Get the current high dpi scale factor rounding policy.

        Returns:
            rounding policy
        """
        return constants.HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY.inverse[
            cls.highDpiScaleFactorRoundingPolicy()
        ]

    @classmethod
    def get_application_state(cls) -> List[constants.ApplicationStateStr]:
        """Get the current application state.

        Returns:
            application state
        """
        return [
            k
            for k, v in constants.APPLICATION_STATES.items()
            if v & cls.applicationState()
        ]

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
