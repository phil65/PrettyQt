from __future__ import annotations

from collections.abc import Iterator
import contextlib
import sys
from typing import SupportsInt

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import colors, datatypes


class GuiApplicationMixin(core.CoreApplicationMixin):
    palette_changed = core.Signal(gui.Palette)

    def event(self, e):
        match e.type():
            case QtCore.QEvent.Type.ApplicationPaletteChange:
                self.palette_changed.emit(gui.Palette(self.palette()))
        return super().event(e)

    @classmethod
    @contextlib.contextmanager
    def override_cursor(cls, cursor: constants.CursorShapeStr):
        cls.set_override_cursor(cursor)
        yield cursor
        cls.restore_override_cursor()

    @classmethod
    def set_override_cursor(cls, cursor: constants.CursorShapeStr):
        crs = gui.Cursor(constants.CURSOR_SHAPE[cursor])
        cls.setOverrideCursor(crs)

    @classmethod
    def restore_override_cursor(cls):
        cls.restoreOverrideCursor()

    @classmethod
    def get_clipboard(cls) -> gui.Clipboard:
        return gui.Clipboard(cls.clipboard())

    @classmethod
    @contextlib.contextmanager
    def edit_palette(cls) -> Iterator[gui.Palette]:
        palette = gui.Palette(cls.palette())
        yield palette
        cls.setPalette(palette)

    @classmethod
    def find_window(cls, h_wnd: SupportsInt) -> QtGui.QWindow:
        for window in cls.topLevelWindows():
            if window and int(window.winId()) == int(h_wnd):
                return window
        return None

    def set_layout_direction(
        self, direction: constants.LayoutDirectionStr | constants.LayoutDirection
    ):
        """Set layout direction.

        Args:
            direction: layout direction
        """
        self.setLayoutDirection(constants.LAYOUT_DIRECTION.get_enum_value(direction))

    def get_layout_direction(self) -> constants.LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return constants.LAYOUT_DIRECTION.inverse[self.layoutDirection()]

    @classmethod
    def set_high_dpi_scale_factor_rounding_policy(
        cls,
        policy: constants.HighDpiScaleFactorRoundingPolicyStr
        | constants.HighDpiScaleFactorRoundingPolicy,
    ):
        """Set high dpi scale factor rounding policy.

        Args:
            policy: rounding policy
        """
        cls.setHighDpiScaleFactorRoundingPolicy(
            constants.HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY.get_enum_value(policy)
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
    def get_application_state(cls) -> list[constants.ApplicationStateStr]:
        """Get the current application state.

        Returns:
            application state
        """
        return [
            k
            for k, v in constants.APPLICATION_STATES.items()
            if v & cls.applicationState()  # type: ignore
        ]

    def get_primary_screen(self) -> gui.Screen:
        return gui.Screen(self.primaryScreen())

    def get_screen_at(self, point: datatypes.PointType) -> gui.Screen:
        p = datatypes.to_point(point)
        return gui.Screen(self.screenAt(p))

    def get_screens(self) -> list[gui.Screen]:
        return [gui.Screen(i) for i in self.screens()]

    @classmethod
    def get_input_method(cls) -> gui.InputMethod:
        return gui.InputMethod(cls.inputMethod())

    @classmethod
    def copy_to_clipboard(cls, text: str):
        """Sets clipboard to supplied text."""
        cb = cls.clipboard()
        cb.clear(mode=cb.Mode.Clipboard)
        cb.setText(text, mode=cb.Mode.Clipboard)

    @classmethod
    def get_font(cls) -> gui.Font:
        return gui.Font(cls.font())

    def set_icon(self, icon: datatypes.IconType):
        """Set the default window icon.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.windowIcon()
        return None if icon.isNull() else gui.Icon(self.windowIcon())

    @classmethod
    def set_palette(cls, palette: constants.ThemeStr | QtGui.QPalette):
        match palette:
            case "default":
                pal = gui.Palette()
            case "dark":
                pal = gui.Palette.create_dark_palette()
            case _:
                pal = palette
        cls.setPalette(pal)

    @classmethod
    def get_keyboard_modifiers(cls) -> list[constants.KeyboardModifierStr]:
        return constants.KEYBOARD_MODIFIERS.get_list(cls.keyboardModifiers())

    @classmethod
    def query_keyboard_modifiers(cls) -> list[constants.KeyboardModifierStr]:
        return constants.KEYBOARD_MODIFIERS.get_list(cls.queryKeyboardModifiers())

    @classmethod
    def get_palette(cls) -> gui.Palette:
        return gui.Palette(cls.palette())

    def set_badge_number(self, number: int | None):
        self.setBadgeNumber(number or 0)

    def set_progress_value(self, value: int, total: int = 100):
        windows = self.topLevelWindows()
        if not windows:
            return None
        if sys.platform.startswith("win"):
            from prettyqt.utils.platforms.windows import taskbaritem

            window_id = windows[0].winId()
            tb = taskbaritem.TaskBarItem(window_id)
            tb.set_progress_value(value, total)


class GuiApplication(GuiApplicationMixin, QtGui.QGuiApplication):
    pass


if __name__ == "__main__":
    app = gui.app()
    app.set_badge_number(5)
    app.exec()
