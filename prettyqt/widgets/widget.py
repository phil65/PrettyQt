from __future__ import annotations

import contextlib
import functools
import os
import pathlib
import sys
from typing import TYPE_CHECKING, Any, Literal

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, colors, datatypes, get_repr, prettyprinter


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


LayoutStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow"]

QWIDGETSIZE_MAX = 16777215  # QtWidgets.QWIDGETSIZE_MAX


class WidgetMixin(core.ObjectMixin):
    box: QtWidgets.QLayout

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "contextMenuPolicy": constants.CONTEXT_POLICY,
            "focusPolicy": constants.FOCUS_POLICY,
            "layoutDirection": constants.LAYOUT_DIRECTION,
            "windowModality": constants.WINDOW_MODALITY,
        }
        return maps

    def __repr__(self) -> str:
        return get_repr(self)

    def add_shortcut(
        self,
        keysequence: datatypes.KeyCombinationType,
        callback: Callable | None = None,
        context: constants.ShortcutContextStr = "window",
    ) -> gui.Shortcut:
        """Add shortcut to widget.

        Adds as shortcut for given callback and context to this widget.

        Args:
            keysequence: Key sequence
            callback: Callback for the shortcut
            context: context for this shortcut

        Returns:
            shortcut object
        """
        if not isinstance(keysequence, QtGui.QKeySequence):
            keysequence = gui.KeySequence(keysequence)
        context = constants.SHORTCUT_CONTEXT[context]
        return gui.Shortcut(keysequence, self, callback, context=context)

    def get_win_id(self) -> int:
        return int(self.winId())

    def resize(self, *size) -> None:
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def insertAction(
        self, position_or_action: int | QtGui.QAction, action: QtGui.QAction
    ):
        """Extend insertAction to also allow int index."""
        if isinstance(position_or_action, int):
            position_or_action = self.actions()[position_or_action]
        super().insertAction(position_or_action, action)

    def add_action(
        self,
        text: str | gui.Action,
        triggered: Callable = None,
        icon: Any | None = None,
        checkable: bool = False,
        checked: bool = False,
        shortcut: str | None = None,
        status_tip: str | None = None,
        tool_tip: str | None = None,
        parent=None,
    ) -> gui.Action:
        """Add an action to the menu.

        Args:
            text: Label for the action
            triggered: gets called when action is triggered
            icon: icon for action
            checkable: as checkbox action
            checked: if checkable, turn on by default
            shortcut: Shortcut for action
            status_tip: Status tip to be shown in status bar
            tool_tip: Widget ToolTip
            parent: parent

        Returns:
            Action added to menu
        """
        if isinstance(text, str):
            action = gui.Action(parent or self, text=text)
            if triggered:
                action.triggered.connect(triggered)
            action.set_icon(icon)
            action.set_shortcut(shortcut)
            if checkable:
                action.setCheckable(True)
                action.setChecked(checked)
            if status_tip is not None:
                action.setStatusTip(status_tip)
            if tool_tip is not None:
                action.setToolTip(tool_tip)
        else:
            action = text
            action.setParent(self)
        self.addAction(action)
        return action

    def add_actions(self, actions: list[QtGui.QAction]):
        for i in actions:
            i.setParent(self)
        self.addActions(actions)

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

    def set_graphics_effect(
        self,
        effect: QtWidgets.QGraphicsEffect
        | Literal["drop_shadow", "blur", "opacity", "colorize"],
        radius: int = 10,
        opacity: int = 0.7,
        strength: int = 0.5,
        color: datatypes.ColorType = "blue",
    ) -> QtWidgets.QGraphicsEffect:
        match effect:
            case "drop_shadow":
                effect = widgets.GraphicsDropShadowEffect(self)
                effect.setBlurRadius(radius)
                effect.setColor(colors.get_color(color))
            case "blur":
                effect = widgets.GraphicsBlurEffect(self)
                effect.setBlurRadius(radius)
            case "opacity":
                effect = widgets.GraphicsOpacityEffect(self)
                effect.setOpacity(opacity)
            case "colorize":
                effect = widgets.GraphicsColorizeEffect(self)
                effect.setColor(colors.get_color(color))
                effect.setStrength(strength)
        self.setGraphicsEffect(effect)
        return effect

    def play_animation(self, animation_type: str, **kwargs) -> QtCore.QPropertyAnimation:
        from prettyqt import custom_animations

        match animation_type:
            case "fade_in":
                anim = custom_animations.FadeInAnimation(**kwargs, parent=self)
                anim.apply_to(self)
            case "bounce":
                anim = custom_animations.BounceAnimation(**kwargs, parent=self)
                anim.apply_to(self)
            case "slide":
                anim = custom_animations.SlideAnimation(**kwargs, parent=self)
                anim.apply_to(self)
            case "property":
                anim = core.PropertyAnimation(parent=self)
                anim.setTargetObject(self)
                anim.set_property_name(kwargs.pop("name"))
                anim.setStartValue(kwargs.pop("start_value"))
                anim.setEndValue(kwargs.pop("end_value"))
                anim.setDuration(kwargs.pop("duration", 1000))
                anim.set_easing(kwargs.pop("easing", "linear"))
        anim.start()
        return anim

    def map_to_global(self, pos_or_rect):
        match pos_or_rect:
            case QtCore.QRect() | QtCore.QRectF():
                top_left = self.mapToGlobal(pos_or_rect.topLeft())
                bottom_right = self.mapToGlobal(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF():
                return super().mapToGlobal(pos_or_rect)
            case int(), int():
                return self.mapToGlobal(QtCore.QPoint(*pos_or_rect))
            case float(), float():
                return self.mapToGlobal(QtCore.QPointF(*pos_or_rect))
            case int(), int(), int(), int():
                return self.map_to_global(QtCore.QRect(*pos_or_rect))
            case float(), float(), float(), float():
                return self.map_to_global(QtCore.QRectF(*pos_or_rect))
            case _:
                raise ValueError(pos_or_rect)

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
        super().setWindowIcon(icon)

    setWindowIcon = set_icon

    def get_icon(self) -> gui.Icon | None:
        icon = super().windowIcon()
        return None if icon.isNull() else gui.Icon(icon)

    def show_tooltip(self, duration: int | None = None):
        if duration is None:
            duration = -1  # automatic
        widgets.ToolTip.showText(
            self.map_to_global((0, 0)), self.toolTip(), msecShowTime=duration
        )

    @functools.singledispatchmethod
    def set_min_size(self, size: QtCore.QSize | tuple[int | None, int | None]) -> None:
        if isinstance(size, tuple):
            x = 0 if size[0] is None else size[0]
            y = 0 if size[1] is None else size[1]
            super().setMinimumSize(x, y)
        else:
            super().setMinimumSize(size)

    setMinimumSize = set_min_size

    @set_min_size.register
    def _(self, x: int, y: int | None):
        self.set_min_size((x, y))

    @set_min_size.register  # these can be merged when min py version is 3.11
    def _(self, x: None, y: int | None):
        self.set_min_size((x, y))

    @functools.singledispatchmethod
    def set_max_size(self, size: QtCore.QSize | tuple[int | None, int | None]) -> None:
        if isinstance(size, tuple):
            x = QWIDGETSIZE_MAX if size[0] is None else size[0]
            y = QWIDGETSIZE_MAX if size[1] is None else size[1]
            super().setMaximumSize(x, y)
        else:
            super().setMaximumSize(size)

    @set_max_size.register
    def _(self, x: int, y: int | None):
        self.set_max_size((x, y))

    @set_max_size.register  # these can be merged when min py version is 3.11
    def _(self, x: None, y: int | None):
        self.set_max_size((x, y))

    def set_min_width(self, width: int | None) -> None:
        if width is None:
            width = 0
        super().setMinimumWidth(width)

    def set_max_width(self, width: int | None) -> None:
        if width is None:
            width = QWIDGETSIZE_MAX
        super().setMaximumWidth(width)

    def set_min_height(self, height: int | None) -> None:
        if height is None:
            height = 0
        super().setMinimumHeight(height)

    def set_max_height(self, height: int | None) -> None:
        if height is None:
            height = QWIDGETSIZE_MAX
        super().setMaximumHeight(height)

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
        tooltip = tooltip.replace("\n", "<br/>")
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

    def set_window_flags(self, *flags: constants.WindowTypeStr, append: bool = False):
        for flag in flags:
            if flag not in constants.WINDOW_TYPE:
                raise InvalidParamError(flag, constants.WINDOW_TYPE)
        result = constants.WINDOW_TYPE.merge_flags(flags)
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

    def set_modality(self, modality: constants.WindowModalityStr) -> None:
        """Set modality for the dialog.

        Args:
            modality: modality for the main window

        Raises:
            InvalidParamError: modality type does not exist
        """
        if modality not in constants.WINDOW_MODALITY:
            raise InvalidParamError(modality, constants.WINDOW_MODALITY)
        self.setWindowModality(constants.WINDOW_MODALITY[modality])

    def get_modality(self) -> constants.WindowModalityStr:
        """Get the current modality modes as a string.

        Returns:
            modality mode
        """
        return constants.WINDOW_MODALITY.inverse[self.windowModality()]

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
    ) -> QtWidgets.QLayout:
        """Quick way to set a layout.

        Sets layout to given layout, also allows setting margin and spacing.

        Args:
            layout: Layout to set
            margin: margin to use in pixels
            spacing: spacing to use in pixels

        Returns:
            Layout
        """
        match layout:
            case None:
                return
            case "horizontal":
                self.box = widgets.HBoxLayout()
            case "vertical":
                self.box = widgets.VBoxLayout()
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
        return self.box

    def position_on(
        self,
        where: Literal["parent", "window", "screen", "mouse"] | QtWidgets.QWidget,
        how: Literal[
            "center",
            "top",
            "left",
            "bottom",
            "right",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
        ] = "center",
        scale_ratio: int | None = None,
        x_offset: int = 0,
        y_offset: int = 0,
    ):
        """Position widget on another widget / window / screen.

        Arguments:
            where: where to positin on
            how: How to align
            scale_ratio: Resize to scale_ratio * target size
            x_offset: additional x offset for final position
            y_offset: additional y offset for final position
        """
        match where:
            case "mouse":
                geom = core.Rect(gui.Cursor.pos(), gui.Cursor.pos())
            case "parent":
                geom = self.parent().frameGeometry()
            case "window":
                geom = self.window().frameGeometry()
            case QtWidgets.QWidget():
                geom = where.frameGeometry()
            case "screen":
                geom = gui.GuiApplication.primaryScreen().geometry()
        if scale_ratio is not None and where != "mouse":
            self.resize(
                int(geom.width() * scale_ratio),
                int(geom.height() * scale_ratio),
            )
        own_geo = self.frameGeometry()
        match how:
            case "center":
                new = geom.center()
            case "top":
                new = core.Point(geom.center().x(), geom.top() + own_geo.height() // 2)
            case "bottom":
                new = core.Point(geom.center().x(), geom.bottom() - own_geo.height() // 2)
            case "left":
                new = core.Point(geom.left() + own_geo.width() // 2, geom.center().y())
            case "right":
                new = core.Point(geom.right() - own_geo.width() // 2, geom.center().y())
            case "top_right":
                new = core.Point(
                    geom.right() - own_geo.width() // 2,
                    geom.top() + own_geo.height() // 2,
                )
            case "top_left":
                new = core.Point(
                    geom.left() + own_geo.width() // 2,
                    geom.top() + own_geo.height() // 2,
                )
            case "bottom_right":
                new = core.Point(
                    geom.right() - own_geo.width() // 2,
                    geom.bottom() - own_geo.height() // 2,
                )
            case "bottom_left":
                new = core.Point(
                    geom.left() + own_geo.width() // 2,
                    geom.bottom() - own_geo.height() // 2,
                )
        new = core.Point(new.x() + x_offset, new.y() + y_offset)
        own_geo.moveCenter(new)
        self.move(own_geo.topLeft())

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

    def set_focus(self, reason: constants.FocusReasonStr | None = None):
        if reason is None:
            self.setFocus()
        else:
            self.setFocus(constants.FOCUS_REASONS[reason])

    def set_font_size(self, size: int) -> None:
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

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
        area: datatypes.RectType | QtGui.QRegion | QtGui.QBitmap | None,
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
        with gui.Painter(image) as painter:
            painter.set_composition_mode("source_atop")
            for gl_widget in self.find_children(QtWidgets.QOpenGLWidget):
                d = gl_widget.mapToGlobal(core.Point()) - self.mapToGlobal(core.Point())
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

    def set_style(self, style: str | QtWidgets.QStyle):
        if isinstance(style, str):
            style = QtWidgets.QStyleFactory.create(style)
        self.setStyle(style)


class Widget(WidgetMixin, prettyprinter.PrettyPrinter, QtWidgets.QWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = Widget()
    widget2 = Widget(
        focus=True, status_tip="trekk", whats_this="kfjk", minimum_width=None
    )
    # widget.play_animation(
    #     "property",
    #     name="windowOpacity",
    #     duration=1000,
    #     start_value=0,
    #     end_value=1,
    # )
    # widget.play_animation("fade_in")
    # val = custom_animations.FadeInAnimation()
    # val.apply_to(widget)
    # val.start()
    widget.set_graphics_effect("colorize")
    widget.show()
    widget2.show()
    app.sleep(4)
    widget.position_on("mouse", scale_ratio=0.5, how="top")
    # widget.add_shortcut("return", print, "application")
    # widget.set_min_size((400, 400))
    # widget.set_max_size(None, 600)
    # print(type(widget.get_screen()))
    app.main_loop()
