from __future__ import annotations

import contextlib
import functools
import os
import html
import pathlib
import sys
from typing import TYPE_CHECKING, Any, Literal, overload

from collections.abc import Sequence

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, colors, datatypes, fx


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from prettyqt import custom_widgets


LayoutStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow", "border"]

QWIDGETSIZE_MAX = 16777215  # QtWidgets.QWIDGETSIZE_MAX

PositionPossibilityType = (
    Literal["parent", "window", "screen", "mouse"]
    | QtWidgets.QWidget
    | QtCore.QRect
    | QtCore.QPoint
    | tuple[int, int]
    | tuple[int, int, int, int]
)


class WidgetMixin(core.ObjectMixin):
    def __init__(self, *args, margin: int | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fx = fx.Fx(self)
        if margin is not None:
            self.set_margin(margin)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "contextMenuPolicy": constants.CONTEXT_POLICY,
            "focusPolicy": constants.FOCUS_POLICY,
            "layoutDirection": constants.LAYOUT_DIRECTION,
            "windowModality": constants.WINDOW_MODALITY,
        }
        return maps

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

    def resize(self, *size):
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_enabled(self, enabled: bool = True) -> None:
        self.setEnabled(enabled)

    def set_disabled(self) -> None:
        self.setEnabled(False)

    def insertAction(
        self, position_or_action: int | QtGui.QAction, action: QtGui.QAction
    ):
        """Extend insertAction to also allow int index."""
        if isinstance(position_or_action, int):
            actions = self.actions()
            if len(actions) == 0 or position_or_action >= len(actions):
                # Insert as the first action or the last action.
                return super().addAction(action)
            position_or_action = actions[position_or_action]
        super().insertAction(position_or_action, action)

    def add_action(
        self,
        text: str | gui.Action,
        parent: QtWidgets.QWidget | None = None,
        data: Any = None,
        **kwargs,
    ) -> gui.Action:
        """Add an action to the menu.

        Args:
            text: Label for the action
            parent: parent
            data: data for the Action
            kwargs: kwargs passed to action ctor
        Returns:
            Action added to menu
        """
        if isinstance(text, str):
            action = gui.Action(parent=parent or self, text=text, **kwargs)
        else:
            action = text
            action.setParent(self)
        self.addAction(action)
        action.setData(data)
        return action

    def add_actions(self, actions: Sequence[QtGui.QAction]):
        for i in actions:
            i.setParent(self)
        self.addActions(actions)

    def toggle_fullscreen(self) -> bool:
        """Toggle between fullscreen and regular size."""
        if self.isFullScreen():
            self.showNormal()
            return False
        else:
            self.showFullScreen()
            return True

    def toggle_maximized(self) -> bool:
        """Toggle between maximized and regular size."""
        if self.isMaximized():
            self.showNormal()
            return False
        else:
            self.showMaximized()
            return True

    def map_to(
        self,
        widget: QtWidgets.QWidget | Literal["global", "parent", "window"],
        pos_or_rect,
    ) -> QtCore.QRect | QtCore.QRectF | QtCore.QPoint | QtCore.QPointF:
        """Map a point or rect to a widget, global position or parent."""
        match pos_or_rect:
            case int(), int():
                pos_or_rect = QtCore.QPoint(*pos_or_rect)
            case float(), float():
                pos_or_rect = QtCore.QPointF(*pos_or_rect)
            case int(), int(), int(), int():
                pos_or_rect = QtCore.QRect(*pos_or_rect)
            case float(), float(), float(), float():
                pos_or_rect = QtCore.QRectF(*pos_or_rect)
        match pos_or_rect, widget:
            case QtCore.QRect() | QtCore.QRectF(), QtWidgets.QWidget():
                top_left = super().mapTo(widget, pos_or_rect.topLeft())
                bottom_right = super().mapTo(widget, pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), QtWidgets.QWidget():
                return super().mapTo(widget, pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "parent":
                top_left = super().mapToParent(pos_or_rect.topLeft())
                bottom_right = super().mapToParent(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "parent":
                return super().mapToParent(pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "window":
                top_left = super().mapTo(self.window(), pos_or_rect.topLeft())
                bottom_right = super().mapTo(self.window(), pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "window":
                return super().mapTo(self.window(), pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "global":
                top_left = super().mapToGlobal(pos_or_rect.topLeft())
                bottom_right = super().mapToGlobal(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "global":
                return super().mapToGlobal(pos_or_rect)
            case _:
                raise ValueError(pos_or_rect)

    def map_from(
        self,
        widget: QtWidgets.QWidget | Literal["global", "parent", "window"],
        pos_or_rect,
    ) -> QtCore.QRect | QtCore.QRectF | QtCore.QPoint | QtCore.QPointF:
        """Map a point or rect from a widget, global position or parent."""
        match pos_or_rect:
            case int(), int():
                pos_or_rect = QtCore.QPoint(*pos_or_rect)
            case float(), float():
                pos_or_rect = QtCore.QPointF(*pos_or_rect)
            case int(), int(), int(), int():
                pos_or_rect = QtCore.QRect(*pos_or_rect)
            case float(), float(), float(), float():
                pos_or_rect = QtCore.QRectF(*pos_or_rect)
        match pos_or_rect, widget:
            case QtCore.QRect() | QtCore.QRectF(), QtWidgets.QWidget():
                top_left = super().mapFrom(widget, pos_or_rect.topLeft())
                bottom_right = super().mapFrom(widget, pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), QtWidgets.QWidget():
                return super().mapFrom(widget, pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "parent":
                top_left = super().mapFromParent(pos_or_rect.topLeft())
                bottom_right = super().mapFromParent(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "parent":
                return super().mapFromParent(pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "window":
                top_left = super().mapFrom(self.window(), pos_or_rect.topLeft())
                bottom_right = super().mapFrom(self.window(), pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "window":
                return super().mapFrom(self.window(), pos_or_rect)
            case QtCore.QRect() | QtCore.QRectF(), "global":
                top_left = super().mapFromGlobal(pos_or_rect.topLeft())
                bottom_right = super().mapFromGlobal(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case QtCore.QPoint() | QtCore.QPointF(), "global":
                return super().mapFromGlobal(pos_or_rect)
            case _:
                raise ValueError(pos_or_rect)

    def raise_to_top(self):
        """Brings a widget to top with all means available."""
        if sys.platform.startswith("win"):
            from prettyqt.utils.platforms.windows import misc

            misc.raise_to_top()
        # state = (self.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive
        # self.setWindowState(state)
        self.raise_()
        self.show()
        self.activateWindow()

    def set_icon(self, icon: datatypes.IconType):
        """Set the window icon.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        super().setWindowIcon(icon)

    setWindowIcon = set_icon

    def get_icon(self) -> gui.Icon | None:
        """Get the window icon (returns None if not existing)."""
        icon = super().windowIcon()
        return None if icon.isNull() else gui.Icon(icon)

    def show_tooltip(self, duration: int | None = None):
        """Show the tooltip of this widget for given time.

        When no duration is given, it will get calculated based on length.
        """
        if duration is None:
            duration = -1  # automatic
        pos = self.map_to("global", (0, 0))
        widgets.ToolTip.showText(pos, self.toolTip(), msecShowTime=duration)

    # lets be gentle and allow all reasonable signatures for the size setters.
    # tuples as well as passing two args is possible.
    @functools.singledispatchmethod
    def set_min_size(self, size: QtCore.QSize | tuple[int | None, int | None]):
        match size:
            case int() | None as x, int() | None as y:
                super().setMinimumSize(x or 0, y or 0)
            case QtCore.QSize():
                super().setMinimumSize(size)
            case _:
                raise TypeError(size)

    setMinimumSize = set_min_size

    @set_min_size.register
    def _(self, x: int, y: int | None):
        self.set_min_size((x, y))

    @set_min_size.register  # these can be merged when min py version is 3.11
    def _(self, x: None, y: int | None):
        self.set_min_size((x, y))

    @functools.singledispatchmethod
    def set_max_size(self, size: QtCore.QSize | tuple[int | None, int | None]):
        match size:
            case int() | None as x, int() | None as y:
                x = QWIDGETSIZE_MAX if x is None else x
                y = QWIDGETSIZE_MAX if y is None else y
                super().setMaximumSize(x, y)
            case _:
                super().setMaximumSize(size)

    setMaximumSize = set_min_size

    @set_max_size.register
    def _(self, x: int, y: int | None):
        self.set_max_size((x, y))

    @set_max_size.register  # these can be merged when min py version is 3.11
    def _(self, x: None, y: int | None):
        self.set_max_size((x, y))

    def set_min_width(self, width: int | None):
        super().setMinimumWidth(width or 0)

    setMinimumWidth = set_min_width

    def set_max_width(self, width: int | None):
        if width is None:
            width = QWIDGETSIZE_MAX
        super().setMaximumWidth(width)

    setMaximumWidth = set_max_width

    def set_min_height(self, height: int | None):
        super().setMinimumHeight(height or 0)

    setMinimumHeight = set_min_height

    def set_max_height(self, height: int | None):
        if height is None:
            height = QWIDGETSIZE_MAX
        super().setMaximumHeight(height)

    setMaximumHeight = set_max_height

    def setWindowTitle(self, title: str):
        if not self.objectName() and widgets.app().is_debug():
            self.setObjectName(title)
        super().setWindowTitle(title)

    def set_title(self, title: str):
        self.setWindowTitle(title)

    def get_title(self) -> str:
        return self.windowTitle()

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
        rich_text: bool = False,
    ):
        """Set a tooltip for this widget.

        In image can get displayed by passing a PathLike object.
        """
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        tooltip = tooltip.replace("\n", "<br/>")
        if rich_text:
            tooltip = f"<html>{html.escape(tooltip)}</html>"
        super().setToolTip(tooltip)

    def set_font(
        self,
        font_name: QtGui.QFont | str | None = None,
        font_size: int | None = None,
        weight: int | None = None,
        italic: bool = False,
    ) -> QtGui.QFont:
        """Set the font for this widget."""
        if isinstance(font_name, QtGui.QFont):
            super().setFont(font_name)
            return font_name
        if font_size is None:
            font_size = -1
        if weight is None:
            weight = -1
        if font_name is None:
            font_name = self.font().family()
        font = gui.Font(font_name, font_size, weight, italic)
        super().setFont(font)
        return font

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_foreground_role(self) -> gui.palette.RoleStr:
        """Set foreground role for this widget."""
        return gui.palette.ROLE.inverse[self.foregroundRole()]

    def set_foreground_role(self, role: gui.palette.RoleStr | gui.Palette.ColorRole):
        """Set foreground role for this widget."""
        self.setForegroundRole(gui.palette.ROLE.get_enum_value(role))

    def get_background_role(self) -> gui.palette.RoleStr:
        """Get background role for this widget."""
        return gui.palette.ROLE.inverse[self.backgroundRole()]

    def set_background_role(self, role: gui.palette.RoleStr | gui.Palette.ColorRole):
        """Get foreground role for this widget."""
        self.setBackgroundRole(gui.palette.ROLE.get_enum_value(role))

    def set_window_flags(self, *flags: constants.WindowTypeStr, append: bool = False):
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
    ):
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

    def set_attribute(self, attribute: constants.WidgetAttributeStr, state: bool = True):
        if attribute not in constants.WIDGET_ATTRIBUTE:
            raise InvalidParamError(attribute, constants.WIDGET_ATTRIBUTE)
        self.setAttribute(constants.WIDGET_ATTRIBUTE[attribute], state)

    def set_attributes(self, **kwargs: bool):
        for attr, state in kwargs.items():
            if attr not in constants.WIDGET_ATTRIBUTE:
                raise InvalidParamError(attr, constants.WIDGET_ATTRIBUTE)
            self.setAttribute(constants.WIDGET_ATTRIBUTE[attr], state)

    def set_modality(
        self, modality: constants.WindowModalityStr | constants.WindowModality
    ):
        """Set modality for the dialog.

        Args:
            modality: modality for the main window
        """
        self.setWindowModality(constants.WINDOW_MODALITY.get_enum_value(modality))

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
    ):
        """Set the size policy.

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
        """Get size policy."""
        qpol = self.sizePolicy()
        if isinstance(qpol, widgets.SizePolicy):
            return qpol
        return widgets.SizePolicy.clone(qpol)

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def set_background_color(self, color: datatypes.ColorType):
        col_str = "" if color is None else colors.get_color(color).name()
        with self.edit_stylesheet() as ss:
            ss.backgroundColor.setValue(col_str)

    @contextlib.contextmanager
    def grab_mouse_events(
        self, cursor_shape: constants.CursorShapeStr | None = None
    ) -> Iterator[None]:
        """Context manager to grab mouse events."""
        if cursor_shape is not None:
            self.grabMouse(constants.CURSOR_SHAPE[cursor_shape])
        else:
            self.grabMouse()
        yield None
        self.releaseMouse()

    @contextlib.contextmanager
    def grab_keyboard_events(self) -> Iterator[None]:
        """Context manager to grab keyboard events."""
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
            case str():
                pass
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

    def set_context_menu_policy(
        self, policy: constants.ContextPolicyStr | constants.ContextMenuPolicy
    ):
        """Set contextmenu policy for given item view.

        Args:
            policy: contextmenu policy to use
        """
        self.setContextMenuPolicy(constants.CONTEXT_POLICY.get_enum_value(policy))

    def get_context_menu_policy(self) -> constants.ContextPolicyStr:
        """Return current contextmenu policy.

        Returns:
            contextmenu policy
        """
        return constants.CONTEXT_POLICY.inverse[self.contextMenuPolicy()]

    def set_window_state(self, state: constants.WindowStateStr | constants.WindowState):
        """Set window state for given item view.

        Args:
            state: window state to use
        """
        self.setWindowState(constants.WINDOW_STATES.get_enum_value(state))

    def get_window_state(self) -> constants.WindowStateStr:
        """Return current window state.

        Returns:
            window state
        """
        return constants.WINDOW_STATES.inverse[self.windowState()]

    def set_custom_menu(self, method: Callable):
        self.set_context_menu_policy("custom")
        self.customContextMenuRequested.connect(method)

    @property
    def box(self):
        return self.layout()

    @box.setter
    def box(self, layout):
        self.set_layout(layout)

    @overload
    def set_layout(
        self, layout: Literal["horizontal"], margin: int | None = None, **kwargs
    ) -> widgets.HBoxLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["vertical"], margin: int | None = None, **kwargs
    ) -> widgets.VBoxLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["grid"], margin: int | None = None, **kwargs
    ) -> widgets.GridLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["border"], margin: int | None = None, **kwargs
    ) -> custom_widgets.BorderLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["flow"], margin: int | None = None, **kwargs
    ) -> custom_widgets.FlowLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["form"], margin: int | None = None, **kwargs
    ) -> widgets.FormLayout:
        pass

    @overload
    def set_layout(
        self, layout: Literal["stacked"], margin: int | None = None, **kwargs
    ) -> widgets.StackedLayout:
        pass

    def set_layout(
        self,
        layout: LayoutStr | QtWidgets.QLayout,
        margin: int | None = None,
        **kwargs,
    ) -> QtWidgets.QLayout:
        """Quick way to set a layout.

        Sets layout to given layout, also allows setting margin and spacing.

        Args:
            layout: Layout to set
            margin: margin to use in pixels
            kwargs: keyword arguments passed to layout

        Returns:
            Layout
        """
        from prettyqt import custom_widgets

        match layout:
            case "horizontal":
                layout = widgets.HBoxLayout(**kwargs)
            case "vertical":
                layout = widgets.VBoxLayout(**kwargs)
            case "grid":
                layout = widgets.GridLayout(**kwargs)
            case "form":
                layout = widgets.FormLayout(**kwargs)
            case "stacked":
                layout = widgets.StackedLayout(**kwargs)
            case "flow":
                layout = custom_widgets.FlowLayout(**kwargs)
            case "border":
                layout = custom_widgets.BorderLayout(**kwargs)
            case QtWidgets.QLayout():
                layout = layout
            case _:
                raise ValueError(f"Invalid Layout {layout}")
        self.setLayout(layout)
        if margin is not None:
            layout.set_margin(margin)
        return layout

    def position_on(
        self,
        where: PositionPossibilityType,
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
        do_scale = True
        match where:
            case "mouse":
                geom = core.Rect(gui.Cursor.pos(), gui.Cursor.pos())
                do_scale = False
            case QtCore.QPoint():
                geom = core.Rect(where, where)
                do_scale = False
            case (int(), int()):
                p = core.Point(*where)
                geom = core.Rect(p, p)
                do_scale = False
            case (int(), int(), int(), int()):
                geom = core.Rect(*where)
            case "parent":
                geom = self.parent().frameGeometry()
            case "window":
                geom = self.window().frameGeometry()
            case QtWidgets.QWidget():
                geom = where.frameGeometry()
            case QtCore.QRect():
                geom = where
            case "screen":
                geom = gui.GuiApplication.primaryScreen().geometry()
            case _:
                raise ValueError(where)
        if scale_ratio is not None and do_scale:
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
            case _:
                raise ValueError(how)
        new = core.Point(new.x() + x_offset, new.y() + y_offset)
        own_geo.moveCenter(new)
        self.move(own_geo.topLeft())

    def set_cursor(self, cursor: constants.CursorShapeStr | QtGui.QCursor):
        if isinstance(cursor, QtGui.QCursor):
            curs = cursor
        elif cursor in constants.CURSOR_SHAPE:
            curs = gui.Cursor(constants.CURSOR_SHAPE[cursor])
        else:
            raise InvalidParamError(cursor, constants.CURSOR_SHAPE)
        self.setCursor(curs)

    def set_focus_policy(self, policy: constants.FocusPolicyStr):
        """Set the way the widget accepts keyboard focus.

        Args:
            policy (str): Focus policy
        """
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

    def set_font_size(self, size: int):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    def get_font_metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self.fontMetrics())

    def get_font_info(self) -> gui.FontInfo:
        return gui.FontInfo(self.fontInfo())

    def set_margin(self, margin: int):
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
            case (int(), int(), int(), int()):
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
        from prettyqt.qt import QtOpenGLWidgets

        image = self.grab()
        with gui.Painter(image) as painter:
            painter.set_composition_mode("source_atop")
            for gl_widget in self.find_children(QtOpenGLWidgets.QOpenGLWidget):
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

    def get_cursor(self) -> gui.Cursor:
        return gui.Cursor(self.cursor())

    def set_style(self, style: str | QtWidgets.QStyle):
        if isinstance(style, str):
            style = QtWidgets.QStyleFactory.create(style)
        self.setStyle(style)

    def child_at(self, *args, typ: type[widgets.QWidget] | None = None):
        """Get child widget at position. If type is given, search parents recursively."""
        child = super().childAt(*args)
        if typ is None or isinstance(child, typ):
            return child
        while child := child.parent():
            if isinstance(child, typ):
                return child


class Widget(WidgetMixin, QtWidgets.QWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.TableView()
    meta = widget.get_metaobject()
    prop = meta.get_property("editTriggers")
    print(list(prop.read(widget)))
    widget2 = Widget(status_tip="trekk", whats_this="kfjk", minimum_width=None)
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
    widget.fx.set_graphics_effect("colorize")
    widget.show()
    widget2.show()
    mainwindow = widgets.MainWindow()
    container = widgets.Widget()
    container.set_layout("horizontal")
    container.box.add(widget)
    container.box.add(widget2)
    mainwindow.setCentralWidget(container)
    mainwindow.show()
    app.sleep(4)
    # widget.position_on("mouse", scale_ratio=0.5, how="top")
    # widget.set_min_size((400, 400))
    # widget.set_max_size(None, 600)
    app.exec()
