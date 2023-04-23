from __future__ import annotations

from collections.abc import Callable, Iterator
import contextlib
import os
import pathlib
import sys
from typing import Any, Literal

from deprecated import deprecated
import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, colors, datatypes, helpers, prettyprinter


LayoutStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow"]


class WidgetMixin(core.ObjectMixin):
    box: QtWidgets.QLayout

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def resize(self, *size) -> None:
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def toggle_fullscreen(self):
        """Toggle between fullscreen and regular size."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_maximized(self):
        """Toggle between maximized and regular size."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def raise_to_top(self):
        if sys.platform.startswith("win"):
            import win32con
            from win32gui import SetWindowPos

            # set to always-on-top and disable it again. that way windows stays in front
            flag = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            win_id = self.winId()
            SetWindowPos(win_id, win32con.HWND_TOPMOST, 0, 0, 0, 0, flag)
            SetWindowPos(win_id, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flag)
        # state = (self.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive
        # self.setWindowState(state)
        self.raise_()
        self.show()
        self.activateWindow()

    def set_icon(self, icon: datatypes.IconType) -> None:
        """Set the window icon.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.windowIcon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_min_size(self, *size) -> None:
        self.setMinimumSize(*size)

    def set_max_size(self, *size) -> None:
        self.setMaximumSize(*size)

    def set_min_width(self, width: int | None) -> None:
        if width is None:
            width = 0
        self.setMinimumWidth(width)

    def set_max_width(self, width: int | None) -> None:
        if width is None:
            width = 16777215  # QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumWidth(width)

    def set_min_height(self, height: int | None) -> None:
        if height is None:
            height = 0
        self.setMinimumHeight(height)

    def set_max_height(self, height: int | None) -> None:
        if height is None:
            height = 16777215  # QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumHeight(height)

    def set_enabled(self, enabled: bool = True) -> None:
        self.setEnabled(enabled)

    def set_disabled(self) -> None:
        self.setEnabled(False)

    def set_title(self, title: str) -> None:
        self.setWindowTitle(title)

    def get_title(self) -> str:
        return self.windowTitle()

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        self.setToolTip(tooltip)

    def set_font(
        self,
        font_name: str | None = None,
        font_size: int | None = None,
        weight: int | None = None,
        italic: bool = False,
    ) -> gui.Font:
        if font_size is None:
            font_size = -1
        if weight is None:
            weight = -1
        if font_name is None:
            font_name = self.font().family()
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)
        return font

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_foreground_role(self) -> gui.palette.RoleStr:
        return gui.palette.ROLE.inverse[self.foregroundRole()]

    def set_foreground_role(self, role: gui.palette.RoleStr):
        if role not in gui.palette.ROLE:
            raise InvalidParamError(role, gui.palette.ROLE)
        self.setForegroundRole(gui.palette.ROLE[role])

    def get_background_role(self) -> gui.palette.RoleStr:
        return gui.palette.ROLE.inverse[self.backgroundRole()]

    def set_background_role(self, role: gui.palette.RoleStr):
        if role not in gui.palette.ROLE:
            raise InvalidParamError(role, gui.palette.ROLE)
        self.setBackgroundRole(gui.palette.ROLE[role])

    def set_window_flags(self, *flags: constants.WindowFlagStr, append: bool = False):
        for flag in flags:
            if flag not in constants.WINDOW_FLAGS:
                raise InvalidParamError(flag, constants.WINDOW_FLAGS)
        result = helpers.merge_flags(flags, constants.WINDOW_FLAGS)
        if append:
            result = result | self.windowFlags()
        self.setWindowFlags(result)

    def set_flags(
        self,
        minimize: bool | None = None,
        maximize: bool | None = None,
        close: bool | None = None,
        stay_on_top: bool | None = None,
        frameless: bool | None = None,
        window: bool | None = None,
        dialog: bool | None = None,
        tooltip: bool | None = None,
        tool: bool | None = None,
        customize: bool | None = None,
        window_title: bool | None = None,
    ) -> None:
        flags = {
            minimize: QtCore.Qt.WindowType.WindowMinimizeButtonHint,
            maximize: QtCore.Qt.WindowType.WindowMaximizeButtonHint,
            close: QtCore.Qt.WindowType.WindowCloseButtonHint,
            stay_on_top: QtCore.Qt.WindowType.WindowStaysOnTopHint,
            frameless: QtCore.Qt.WindowType.FramelessWindowHint,
            window: QtCore.Qt.WindowType.Window,
            dialog: QtCore.Qt.WindowType.Dialog,
            tooltip: QtCore.Qt.WindowType.ToolTip,
            tool: QtCore.Qt.WindowType.Tool,
            customize: QtCore.Qt.WindowType.CustomizeWindowHint,
            window_title: QtCore.Qt.WindowType.WindowTitleHint,
        }
        for k, v in flags.items():
            if k is not None:
                self.setWindowFlag(v, k)

    def set_attribute(
        self, attribute: constants.WidgetAttributeStr, state: bool = True
    ) -> None:
        if attribute not in constants.WIDGET_ATTRIBUTE:
            raise InvalidParamError(attribute, constants.WIDGET_ATTRIBUTE)
        self.setAttribute(constants.WIDGET_ATTRIBUTE[attribute], state)

    def set_attributes(self, **kwargs: bool) -> None:
        for attr, state in kwargs.items():
            if attr not in constants.WIDGET_ATTRIBUTE:
                raise InvalidParamError(attr, constants.WIDGET_ATTRIBUTE)
            self.setAttribute(constants.WIDGET_ATTRIBUTE[attr], state)  # type: ignore

    def set_modality(self, modality: constants.ModalityStr) -> None:
        """Set modality for the dialog.

        Args:
            modality: modality for the main window

        Raises:
            InvalidParamError: modality type does not exist
        """
        if modality not in constants.MODALITY:
            raise InvalidParamError(modality, constants.MODALITY)
        self.setWindowModality(constants.MODALITY[modality])

    def get_modality(self) -> constants.ModalityStr:
        """Get the current modality modes as a string.

        Returns:
            modality mode
        """
        return constants.MODALITY.inverse[self.windowModality()]

    def set_size_policy(
        self,
        horizontal: widgets.sizepolicy.SizePolicyStr | None = None,
        vertical: widgets.sizepolicy.SizePolicyStr | None = None,
    ) -> None:
        """Set the sizes policy.

        Args:
            horizontal: horizontal size policy
            vertical: vertical size policy
        """
        sp = self.get_size_policy()
        if horizontal is not None:
            sp.set_horizontal_policy(horizontal)
        if vertical is not None:
            sp.set_vertical_policy(vertical)
        self.setSizePolicy(sp)

    def get_size_policy(self) -> widgets.SizePolicy:
        qpol = self.sizePolicy()
        if isinstance(qpol, widgets.SizePolicy):
            return qpol
        return widgets.SizePolicy.clone(qpol)

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def set_background_color(self, color: datatypes.ColorType) -> None:
        col_str = "" if color is None else colors.get_color(color).name()
        with self.edit_stylesheet() as ss:
            ss.backgroundColor.setValue(col_str)

    @contextlib.contextmanager
    def grab_mouse_events(
        self, cursor_shape: constants.CursorShapeStr | None = None
    ) -> Iterator[None]:
        if cursor_shape is not None:
            self.grabMouse(constants.CURSOR_SHAPE[cursor_shape])
        else:
            self.grabMouse()
        yield None
        self.releaseMouse()

    @contextlib.contextmanager
    def grab_keyboard_events(self) -> Iterator[None]:
        self.grabKeyboard()
        yield None
        self.releaseKeyboard()

    @contextlib.contextmanager
    def updates_off(self) -> Iterator[None]:
        updates = self.updatesEnabled()
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(updates)

    @contextlib.contextmanager
    def edit_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        ss = self.get_stylesheet()
        yield ss
        self.set_stylesheet(ss)

    def set_stylesheet(
        self, ss: None | str | qstylizer.style.StyleSheet | datatypes.PathType
    ):
        match ss:
            case None:
                ss = ""
            case os.PathLike():
                ss = pathlib.Path(ss).read_text()
            case qstylizer.style.StyleSheet():
                ss = str(ss)
        self.setStyleSheet(ss)

    def get_stylesheet(self) -> qstylizer.style.StyleSheet:
        try:
            return qstylizer.parser.parse(self.styleSheet())
        except ValueError:
            return qstylizer.style.StyleSheet()

    @contextlib.contextmanager
    def edit_palette(self) -> Iterator[gui.Palette]:
        palette = gui.Palette(self.palette())
        yield palette
        self.setPalette(palette)

    @contextlib.contextmanager
    def edit_font(self) -> Iterator[gui.Font]:
        font = gui.Font(self.font())
        yield font
        self.setFont(font)

    @deprecated(reason="This context manager is deprecated, use edit_font instead.")
    @contextlib.contextmanager
    def current_font(self) -> Iterator[gui.Font]:
        with self.edit_font() as font:
            yield font

    @deprecated(reason="This method is deprecated, use set_context_menu_policy instead.")
    def set_contextmenu_policy(self, policy: constants.ContextPolicyStr) -> None:
        return self.set_context_menu_policy(policy)

    def set_context_menu_policy(self, policy: constants.ContextPolicyStr) -> None:
        """Set contextmenu policy for given item view.

        Args:
            policy: contextmenu policy to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in constants.CONTEXT_POLICY:
            raise InvalidParamError(policy, constants.CONTEXT_POLICY)
        self.setContextMenuPolicy(constants.CONTEXT_POLICY[policy])

    @deprecated(reason="This method is deprecated, use get_context_menu_policy instead.")
    def get_contextmenu_policy(self) -> constants.ContextPolicyStr:
        """Return current contextmenu policy.

        Returns:
            contextmenu policy
        """
        return self.get_context_menu_policy()

    def get_context_menu_policy(self) -> constants.ContextPolicyStr:
        """Return current contextmenu policy.

        Returns:
            contextmenu policy
        """
        return constants.CONTEXT_POLICY.inverse[self.contextMenuPolicy()]

    def set_window_state(self, policy: constants.WindowStateStr) -> None:
        """Set window state for given item view.

        Args:
            policy: window state to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in constants.WINDOW_STATES:
            raise InvalidParamError(policy, constants.WINDOW_STATES)
        self.setWindowState(constants.WINDOW_STATES[policy])

    def get_window_state(self) -> constants.WindowStateStr:
        """Return current window state.

        Returns:
            window state
        """
        return constants.WINDOW_STATES.inverse[self.windowState()]

    def set_custom_menu(self, method: Callable) -> None:
        self.set_context_menu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(
        self,
        layout: LayoutStr | QtWidgets.QLayout | None,
        margin: int | None = None,
        spacing: int | None = None,
    ):
        if layout is None:
            return
        match layout:
            case "horizontal" | "vertical":
                self.box = widgets.BoxLayout(layout)
            case "grid":
                self.box = widgets.GridLayout()
            case "form":
                self.box = widgets.FormLayout()
            case "stacked":
                self.box = widgets.StackedLayout()
            case "flow":
                from prettyqt import custom_widgets

                self.box = custom_widgets.FlowLayout()
            case QtWidgets.QLayout():
                self.box = layout
            case _:
                raise ValueError("Invalid Layout")
        self.setLayout(self.box)
        if margin is not None:
            self.box.set_margin(margin)
        if spacing is not None:
            self.box.setSpacing(spacing)

    def center(self, screen: int = 0) -> None:
        qr = self.frameGeometry()
        cp = gui.GuiApplication.screens()[screen].geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_cursor(self, cursor: constants.CursorShapeStr | QtGui.QCursor) -> None:
        if isinstance(cursor, QtGui.QCursor):
            curs = cursor
        elif cursor in constants.CURSOR_SHAPE:
            curs = gui.Cursor(constants.CURSOR_SHAPE[cursor])
        else:
            raise InvalidParamError(cursor, constants.CURSOR_SHAPE)
        self.setCursor(curs)

    def set_focus_policy(self, policy: constants.FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy (str): Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in constants.FOCUS_POLICY:
            raise InvalidParamError(policy, constants.FOCUS_POLICY)
        self.setFocusPolicy(constants.FOCUS_POLICY[policy])

    def get_focus_policy(self) -> constants.FocusPolicyStr:
        """Return waay the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return constants.FOCUS_POLICY.inverse[self.focusPolicy()]

    def set_font_size(self, size: int) -> None:
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    @deprecated(reason="This method is deprecated, use get_font_metrics instead.")
    def font_metrics(self) -> gui.FontMetrics:
        return self.get_font_metrics()

    def get_font_metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self.fontMetrics())

    def get_font_info(self) -> gui.FontInfo:
        return gui.FontInfo(self.fontInfo())

    def set_margin(self, margin: int) -> None:
        self.setContentsMargins(margin, margin, margin, margin)

    def raise_dock(self) -> bool:
        w = self.find_parent(QtWidgets.QDockWidget)
        if w is None:
            return False
        w.setVisible(True)
        w.raise_()
        return True

    def set_mask(
        self,
        area: datatypes.RectType | QtGui.QRegion | None,
        typ: gui.region.RegionTypeStr = "rectangle",
    ):
        match area:
            case None:
                self.clearMask()
                return
            case tuple():
                area = gui.Region(*area, gui.region.REGION_TYPE[typ])
            case QtCore.QRect():
                area = gui.Region(area, gui.region.REGION_TYPE[typ])
        self.setMask(area)

    def set_window_file_path(self, path: datatypes.PathType):
        self.setWindowFilePath(os.fspath(path))

    def get_window_file_path(self) -> pathlib.Path | None:
        path = self.windowFilePath()
        return pathlib.Path(path) if path else None

    def get_image(self) -> QtGui.QPixmap:
        image = self.grab()
        if gl_widget := self.find_child(QtWidgets.QOpenGLWidget):
            d = gl_widget.mapToGlobal(core.Point()) - self.mapToGlobal(core.Point())
            with gui.Painter(image) as painter:
                painter.set_composition_mode("source_atop")
                painter.drawImage(d, gl_widget.grabFramebuffer())
        return image

    def get_screen(self) -> gui.Screen | None:
        window = self.window().windowHandle()
        return None if window is None else gui.Screen(window.screen())

    def delete_children(self):
        """Delete all children of the specified QObject."""
        if hasattr(self, "clear"):
            return self.clear()
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            if widget := item.widget():
                widget.deleteLater()
            else:
                self.delete_children(item.layout())

    def get_cursor(self) -> gui.Cursor:
        return gui.Cursor(self.cursor())


class Widget(WidgetMixin, prettyprinter.PrettyPrinter, QtWidgets.QWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = Widget()
    widget.show()
    print(type(widget.get_screen()))
    app.main_loop()
