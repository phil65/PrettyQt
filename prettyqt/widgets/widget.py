from __future__ import annotations

from collections.abc import Sequence
import contextlib
import functools
import html
import os
import pathlib
import sys

from typing import TYPE_CHECKING, Any, Literal, overload

import qstylizer.parser
import qstylizer.style

from prettyqt import constants, core, gui, iconprovider, widgets
from prettyqt.utils import colors, datatypes, fx


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from prettyqt import custom_widgets


LayoutStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow", "border"]

QWIDGETSIZE_MAX = 16_777_215  # widgets.QWIDGETSIZE_MAX

PositionPossibilityType = (
    Literal["parent", "window", "screen", "mouse"]
    | widgets.QWidget
    | core.QRect
    | core.QPoint
    | tuple[int, int]
    | tuple[int, int, int, int]
)


class WidgetMixin(core.ObjectMixin):
    def __init__(self, *args, margin: int | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fx = fx.Fx(self)
        if margin is not None:
            self.set_margin(margin)

    @classmethod
    def setup_example(cls):
        return cls()

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
        return gui.Shortcut(
            datatypes.to_keysequence(keysequence),
            self,
            callback,
            context=constants.SHORTCUT_CONTEXT.get_enum_value(context),
        )

    def get_win_id(self) -> int:
        return int(self.winId())

    def resize(self, *size):
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_width(self, width: int):
        self.resize(width, self.height())

    def set_height(self, height: int):
        self.resize(self.width(), height)

    def set_enabled(self, enabled: bool = True) -> None:
        self.setEnabled(enabled)

    def set_disabled(self) -> None:
        self.setEnabled(False)

    def insertAction(self, position_or_action: int | gui.QAction, action: gui.QAction):
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
        parent: widgets.QWidget | None = None,
        data: Any = None,
        **kwargs: datatypes.VariantType,
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

    def add_actions(self, actions: Sequence[gui.QAction]):
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
        widget: widgets.QWidget | Literal["global", "parent", "window"],
        pos_or_rect: datatypes.PointType
        | datatypes.RectType
        | datatypes.PointFType
        | datatypes.RectFType,
    ) -> core.QRect | core.QRectF | core.QPoint | core.QPointF:
        """Map a point or rect to a widget, global position or parent.

        Arguments:
            widget: What to map to.
            pos_or_rect: Point or rect to map.
        """
        match pos_or_rect:
            case int(), int():
                pos_or_rect = core.QPoint(*pos_or_rect)
            case float(), float():
                pos_or_rect = core.QPointF(*pos_or_rect)
            case int(), int(), int(), int():
                pos_or_rect = core.QRect(*pos_or_rect)
            case float(), float(), float(), float():
                pos_or_rect = core.QRectF(*pos_or_rect)
        match pos_or_rect, widget:
            case core.QRect() | core.QRectF(), widgets.QWidget():
                top_left = super().mapTo(widget, pos_or_rect.topLeft())
                bottom_right = super().mapTo(widget, pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), widgets.QWidget():
                return super().mapTo(widget, pos_or_rect)
            case core.QRect() | core.QRectF(), "parent":
                top_left = super().mapToParent(pos_or_rect.topLeft())
                bottom_right = super().mapToParent(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "parent":
                return super().mapToParent(pos_or_rect)
            case core.QRect() | core.QRectF(), "window":
                top_left = super().mapTo(self.window(), pos_or_rect.topLeft())
                bottom_right = super().mapTo(self.window(), pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "window":
                return super().mapTo(self.window(), pos_or_rect)
            case core.QRect() | core.QRectF(), "global":
                top_left = super().mapToGlobal(pos_or_rect.topLeft())
                bottom_right = super().mapToGlobal(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "global":
                return super().mapToGlobal(pos_or_rect)
            case _:
                raise ValueError(pos_or_rect)

    def map_from(
        self,
        widget: widgets.QWidget | Literal["global", "parent", "window"],
        pos_or_rect: datatypes.PointType
        | datatypes.RectType
        | datatypes.PointFType
        | datatypes.RectFType,
    ) -> core.QRect | core.QRectF | core.QPoint | core.QPointF:
        """Map a point or rect from a widget, global position or parent.

        Arguments:
            widget: What to map from.
            pos_or_rect: Point or rect to map.
        """
        match pos_or_rect:
            case int(), int():
                pos_or_rect = core.QPoint(*pos_or_rect)
            case float(), float():
                pos_or_rect = core.QPointF(*pos_or_rect)
            case int(), int(), int(), int():
                pos_or_rect = core.QRect(*pos_or_rect)
            case float(), float(), float(), float():
                pos_or_rect = core.QRectF(*pos_or_rect)
        match pos_or_rect, widget:
            case core.QRect() | core.QRectF(), widgets.QWidget():
                top_left = super().mapFrom(widget, pos_or_rect.topLeft())
                bottom_right = super().mapFrom(widget, pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), widgets.QWidget():
                return super().mapFrom(widget, pos_or_rect)
            case core.QRect() | core.QRectF(), "parent":
                top_left = super().mapFromParent(pos_or_rect.topLeft())
                bottom_right = super().mapFromParent(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "parent":
                return super().mapFromParent(pos_or_rect)
            case core.QRect() | core.QRectF(), "window":
                top_left = super().mapFrom(self.window(), pos_or_rect.topLeft())
                bottom_right = super().mapFrom(self.window(), pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "window":
                return super().mapFrom(self.window(), pos_or_rect)
            case core.QRect() | core.QRectF(), "global":
                top_left = super().mapFromGlobal(pos_or_rect.topLeft())
                bottom_right = super().mapFromGlobal(pos_or_rect.bottomRight())
                return type(pos_or_rect)(top_left, bottom_right)
            case core.QPoint() | core.QPointF(), "global":
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
        color = widgets.app().get_window_icon_color()
        icon = iconprovider.get_icon(icon, color=color)
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
    def set_min_size(self, size: core.QSize | tuple[int | None, int | None]):
        match size:
            case int() | None as x, int() | None as y:
                super().setMinimumSize(x or 0, y or 0)
            case core.QSize():
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
    def set_max_size(self, size: core.QSize | tuple[int | None, int | None]):
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
                if isinstance(size, core.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        tooltip = tooltip.replace("\n", "<br/>")
        if rich_text:
            tooltip = f"<html>{html.escape(tooltip)}</html>"
        super().setToolTip(tooltip)

    def set_font(
        self,
        font_name: gui.QFont | str | None = None,
        font_size: int | None = None,
        weight: int | None = None,
        italic: bool = False,
    ) -> gui.QFont:
        """Set the font for this widget."""
        if isinstance(font_name, gui.QFont):
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
        cover: bool | None = None,
        window_title: bool | None = None,
    ):
        """Set window flags.

        Arguments:
            minimize: set WindowMinimizeButtonHint flag
            maximize: set WindowMaximizeButtonHint flag
            close: set WindowCloseButtonHint flag
            stay_on_top: set WindowStaysOnTopHint flag
            frameless: set FramelessWindowHint flag
            window: set Window flag
            dialog: set Dialog flag
            tooltip: set ToolTip flag
            tool: set Tool flag
            customize: set CustomizeWindowHint flag
            cover: set CoverWindow flag
            window_title: set WindowTitleHint flag
        """
        flags = {
            constants.WindowType.WindowMinimizeButtonHint: minimize,
            constants.WindowType.WindowMaximizeButtonHint: maximize,
            constants.WindowType.WindowCloseButtonHint: close,
            constants.WindowType.WindowStaysOnTopHint: stay_on_top,
            constants.WindowType.FramelessWindowHint: frameless,
            constants.WindowType.Window: window,
            constants.WindowType.Dialog: dialog,
            constants.WindowType.ToolTip: tooltip,
            constants.WindowType.Tool: tool,
            constants.WindowType.CustomizeWindowHint: customize,
            constants.WindowType.CoverWindow: cover,
            constants.WindowType.WindowTitleHint: window_title,
        }
        for k, v in flags.items():
            if v is not None:
                self.setWindowFlag(k, v)

    def set_attributes(
        self,
        accept_drops: bool | None = None,
        always_show_tooltips: bool | None = None,
        custom_whats_this: bool | None = None,
        delete_on_close: bool | None = None,
        disabled: bool | None = None,
        dont_show_on_screen: bool | None = None,
        force_disabled: bool | None = None,
        force_updates_disabled: bool | None = None,
        hover: bool | None = None,
        input_method_enabled: bool | None = None,
        keyboard_focus_change: bool | None = None,
        key_compression: bool | None = None,
        layout_on_entire_rect: bool | None = None,
        layout_uses_widget_rect: bool | None = None,
        mapped: bool | None = None,
        mouse_no_mask: bool | None = None,
        mouse_tracking: bool | None = None,
        moved: bool | None = None,
        no_child_events_for_parent: bool | None = None,
        no_child_events_from_children: bool | None = None,
        no_mouse_replay: bool | None = None,
        no_mouse_propagation: bool | None = None,
        transparent_for_mouse_events: bool | None = None,
        no_system_background: bool | None = None,
        opaque_paint_event: bool | None = None,
        outside_ws_range: bool | None = None,
        paint_on_screen: bool | None = None,
        paint_unclipped: bool | None = None,
        pending_move_event: bool | None = None,
        pending_resize_egent: bool | None = None,
        quit_on_close: bool | None = None,
        resized: bool | None = None,
        right_to_left: bool | None = None,
        set_cursor: bool | None = None,
        set_font: bool | None = None,
        set_palette: bool | None = None,
        set_style: bool | None = None,
        static_contents: bool | None = None,
        style_sheet: bool | None = None,
        style_sheet_target: bool | None = None,
        tablet_tracking: bool | None = None,
        translucent_background: bool | None = None,
        under_mouse: bool | None = None,
        updates_disabled: bool | None = None,
        window_modified: bool | None = None,
        window_propagation: bool | None = None,
        mac_always_show_tool_window: bool | None = None,
        set_locale: bool | None = None,
        styled_background: bool | None = None,
        show_without_activating: bool | None = None,
        native_window: bool | None = None,
        dont_create_native_ancestors: bool | None = None,
        accept_touch_events: bool | None = None,
        touch_pad_single_touch_events: bool | None = None,
        always_stack_on_top: bool | None = None,
        contents_margins_respects_safe_area: bool | None = None,
    ):
        """Set window attributes.

        Attributes:
            accept_drops: set AcceptDrops attribute
            always_show_tooltips: set AlwaysShowToolTips attribute
            custom_whats_this: set CustomWhatsThis attribute
            delete_on_close: set DeleteOnClose attribute
            disabled: set Disabled attribute
            dont_show_on_screen: set DontShowOnScreen attribute
            force_disabled: set ForceDisabled attribute
            force_updates_disabled: set ForceUpdatesDisabled attribute
            hover: set Hover attribute
            input_method_enabled: set InputMethodEnabled attribute
            keyboard_focus_change: set KeyboardFocusChange attribute
            key_compression: set KeyCompression attribute
            layout_on_entire_rect: set LayoutOnEntireRect attribute
            layout_uses_widget_rect: set LayoutUsesWidgetRect attribute
            mapped: set Mapped attribute
            mouse_no_mask: set MouseNoMask attribute
            mouse_tracking: set MouseTracking attribute
            moved: set Moved attribute
            no_child_events_for_parent: set NoChildEventsForParent attribute
            no_child_events_from_children: set NoChildEventsFromChildren attribute
            no_mouse_replay: set NoMouseReplay attribute
            no_mouse_propagation: set NoMousePropagation attribute
            transparent_for_mouse_events: set TransparentForMouseEvents attribute
            no_system_background: set NoSystemBackground attribute
            opaque_paint_event: set OpaquePaintEvent attribute
            outside_ws_range: set OutsideWSRange attribute
            paint_on_screen: set PaintOnScreen attribute
            paint_unclipped: set PaintUnclipped attribute
            pending_move_event: set PendingMoveEvent attribute
            pending_resize_egent: set PendingResizeEvent attribute
            quit_on_close: set QuitOnClose attribute
            resized: set Resized attribute
            right_to_left: set RightToLeft attribute
            set_cursor: set SetCursor attribute
            set_font: set SetFont attribute
            set_palette: set SetPalette attribute
            set_style: set SetStyle attribute
            static_contents: set StaticContents attribute
            style_sheet: set StyleSheet attribute
            style_sheet_target: set StyleSheetTarget attribute
            tablet_tracking: set TabletTracking attribute
            translucent_background: set TranslucentBackground attribute
            under_mouse: set UnderMouse attribute
            updates_disabled: set UpdatesDisabled attribute
            window_modified: set WindowModified attribute
            window_propagation: set WindowPropagation attribute
            mac_always_show_tool_window: set MacAlwaysShowToolWindow attribute
            set_locale: set SetLocale attribute
            styled_background: set StyledBackground attribute
            show_without_activating: set ShowWithoutActivating attribute
            native_window: set NativeWindow attribute
            dont_create_native_ancestors: set DontCreateNativeAncestors attribute
            accept_touch_events: set AcceptTouchEvents attribute
            touch_pad_single_touch_events: set TouchPadAcceptSingleTouchEvents attribute
            always_stack_on_top: set AlwaysStackOnTop attribute
            contents_margins_respects_safe_area: set ContentsMarginsRespectsSafeArea
                                                 attribute
        """
        Attr = constants.WidgetAttribute
        flags = {
            Attr.WA_AcceptDrops: accept_drops,
            Attr.WA_AlwaysShowToolTips: always_show_tooltips,
            Attr.WA_CustomWhatsThis: custom_whats_this,
            Attr.WA_DeleteOnClose: delete_on_close,
            Attr.WA_Disabled: disabled,
            Attr.WA_DontShowOnScreen: dont_show_on_screen,
            Attr.WA_ForceDisabled: force_disabled,
            Attr.WA_ForceUpdatesDisabled: force_updates_disabled,
            Attr.WA_Hover: hover,
            Attr.WA_InputMethodEnabled: input_method_enabled,
            Attr.WA_KeyboardFocusChange: keyboard_focus_change,
            Attr.WA_KeyCompression: key_compression,
            Attr.WA_LayoutOnEntireRect: layout_on_entire_rect,
            Attr.WA_LayoutUsesWidgetRect: layout_uses_widget_rect,
            Attr.WA_Mapped: mapped,
            Attr.WA_MouseNoMask: mouse_no_mask,
            Attr.WA_MouseTracking: mouse_tracking,
            Attr.WA_Moved: moved,
            Attr.WA_NoChildEventsForParent: no_child_events_for_parent,
            Attr.WA_NoChildEventsFromChildren: no_child_events_from_children,
            Attr.WA_NoMouseReplay: no_mouse_replay,
            Attr.WA_NoMousePropagation: no_mouse_propagation,
            Attr.WA_TransparentForMouseEvents: transparent_for_mouse_events,
            Attr.WA_NoSystemBackground: no_system_background,
            Attr.WA_OpaquePaintEvent: opaque_paint_event,
            Attr.WA_OutsideWSRange: outside_ws_range,
            Attr.WA_PaintOnScreen: paint_on_screen,
            Attr.WA_PaintUnclipped: paint_unclipped,
            Attr.WA_PendingMoveEvent: pending_move_event,
            Attr.WA_PendingResizeEvent: pending_resize_egent,
            Attr.WA_QuitOnClose: quit_on_close,
            Attr.WA_Resized: resized,
            Attr.WA_RightToLeft: right_to_left,
            Attr.WA_SetCursor: set_cursor,
            Attr.WA_SetFont: set_font,
            Attr.WA_SetPalette: set_palette,
            Attr.WA_SetStyle: set_style,
            Attr.WA_StaticContents: static_contents,
            Attr.WA_StyleSheet: style_sheet,
            Attr.WA_StyleSheetTarget: style_sheet_target,
            Attr.WA_TabletTracking: tablet_tracking,
            Attr.WA_TranslucentBackground: translucent_background,
            Attr.WA_UnderMouse: under_mouse,
            Attr.WA_UpdatesDisabled: updates_disabled,
            Attr.WA_WindowModified: window_modified,
            Attr.WA_WindowPropagation: window_propagation,
            Attr.WA_MacAlwaysShowToolWindow: mac_always_show_tool_window,
            Attr.WA_SetLocale: set_locale,
            Attr.WA_StyledBackground: styled_background,
            Attr.WA_ShowWithoutActivating: show_without_activating,
            Attr.WA_NativeWindow: native_window,
            Attr.WA_DontCreateNativeAncestors: dont_create_native_ancestors,
            Attr.WA_AcceptTouchEvents: accept_touch_events,
            Attr.WA_TouchPadAcceptSingleTouchEvents: touch_pad_single_touch_events,
            Attr.WA_AlwaysStackOnTop: always_stack_on_top,
            Attr.WA_ContentsMarginsRespectsSafeArea: contents_margins_respects_safe_area,
        }
        for k, v in flags.items():
            if v is not None:
                self.setAttribute(k, v)

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
        horizontal: widgets.sizepolicy.SizePolicyStr
        | widgets.QSizePolicy.Policy
        | None = None,
        vertical: widgets.sizepolicy.SizePolicyStr
        | widgets.QSizePolicy.Policy
        | None = None,
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
        """Context manager to turn off updates for this widget."""
        updates = self.updatesEnabled()
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(updates)

    @contextlib.contextmanager
    def edit_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        """Context manager to edit the stylesheet (using qstylizer)."""
        ss = self.get_stylesheet()
        yield ss
        self.set_stylesheet(ss)

    def set_stylesheet(
        self, ss: None | str | qstylizer.style.StyleSheet | datatypes.PathType
    ):
        """Set stylesheet for this widget."""
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
        """Get current stylesheet."""
        try:
            return qstylizer.parser.parse(self.styleSheet())
        except ValueError:
            return qstylizer.style.StyleSheet()

    @contextlib.contextmanager
    def edit_palette(self) -> Iterator[gui.Palette]:
        """Context manager to edit the palette of the widget."""
        palette = gui.Palette(self.palette())
        yield palette
        self.setPalette(palette)

    @contextlib.contextmanager
    def edit_font(self) -> Iterator[gui.Font]:
        """Context manager to edit the font of the widget."""
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
    def box(self) -> widgets.Layout:
        return self.layout()

    @box.setter
    def box(self, layout: widgets.Layout):
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
        layout: LayoutStr | widgets.QLayout,
        margin: int | None = None,
        **kwargs: datatypes.VariantType,
    ) -> widgets.QLayout:
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
            case widgets.QLayout():
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
            case core.QPoint():
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
            case widgets.QWidget():
                geom = where.frameGeometry()
            case core.QRect():
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

    def set_cursor(
        self, cursor: constants.CursorShapeStr | constants.CursorShape | gui.QCursor
    ):
        """Set the cursor for this widget."""
        if isinstance(cursor, gui.QCursor):
            curs = cursor
        else:
            curs = gui.Cursor(constants.CURSOR_SHAPE.get_enum_value(cursor))
        self.setCursor(curs)

    def set_focus_policy(self, policy: constants.FocusPolicyStr | constants.FocusPolicy):
        """Set the way the widget accepts keyboard focus.

        Args:
            policy (str): Focus policy
        """
        self.setFocusPolicy(constants.FOCUS_POLICY.get_enum_value(policy))

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

    def set_margin(self, margin: datatypes.MarginsType):
        """Set content margins for the widget.

        Arguments:
            margin: margins to use
        """
        self.setContentsMargins(datatypes.to_margins(margin))

    def raise_dock(self) -> bool:
        w = self.find_parent(widgets.QDockWidget)
        if w is None:
            return False
        w.setVisible(True)
        w.raise_()
        return True

    def set_mask(
        self,
        area: datatypes.RectType | gui.QRegion | gui.QBitmap | None,
        typ: gui.region.RegionTypeStr = "rectangle",
    ):
        """Set mask of the widget.

        Arguments:
            area: Mask area
            typ: type of region (only used if area is a QRegion)
        """
        match area:
            case None:
                self.clearMask()
                return
            case (int(), int(), int(), int()):
                area = gui.Region(*area, gui.region.REGION_TYPE[typ])
            case core.QRect():
                area = gui.Region(area, gui.region.REGION_TYPE[typ])
        self.setMask(area)

    def set_window_file_path(self, path: datatypes.PathType):
        self.setWindowFilePath(os.fspath(path))

    def get_window_file_path(self) -> pathlib.Path | None:
        path = self.windowFilePath()
        return pathlib.Path(path) if path else None

    def get_image(self) -> gui.QPixmap:
        """Get a pixmap for the widget.

        Implements a workaround to also include QOpenGlWidgets.
        """
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

    def set_style(self, style: str | widgets.QStyle):
        """Set widget style."""
        if isinstance(style, str):
            style = widgets.QStyleFactory.create(style)
        self.setStyle(style)

    def child_at(self, *args, typ: type[widgets.QWidget] | None = None):
        """Get child widget at position. If type is given, search parents recursively."""
        child = super().childAt(*args)
        if typ is None or isinstance(child, typ):
            return child
        while child := child.parent():
            if isinstance(child, typ):
                return child

    def set_layout_direction(
        self, direction: constants.LayoutDirectionStr | constants.LayoutDirection | None
    ):
        """Set layout direction.

        Args:
            direction: layout direction
        """
        if direction is None:
            self.unsetLayoutDirection()
        else:
            self.setLayoutDirection(constants.LAYOUT_DIRECTION.get_enum_value(direction))

    def get_layout_direction(self) -> constants.LayoutDirectionStr:
        """Get the current layout direction.

        Returns:
            layout direction
        """
        return constants.LAYOUT_DIRECTION.inverse[self.layoutDirection()]


class Widget(WidgetMixin, widgets.QWidget):
    """The base class of all user interface objects."""


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
    # val = animations.FadeInAnimation()
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
