from contextlib import contextmanager

from typing import Dict, Iterator, Callable, Optional, Union, Any, Literal

from qtpy import QtCore, QtGui, QtWidgets
import qstylizer.parser
import qstylizer.style
from deprecated import deprecated

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, colors, InvalidParamError, helpers, prettyprinter


CONTEXT_POLICY = bidict(
    none=QtCore.Qt.NoContextMenu,
    prevent=QtCore.Qt.PreventContextMenu,
    default=QtCore.Qt.DefaultContextMenu,
    actions=QtCore.Qt.ActionsContextMenu,
    custom=QtCore.Qt.CustomContextMenu,
    # showhide_menu="showhide_menu",
)

ContextPolicyStr = Literal["none", "prevent", "default", "actions", "custom"]

MODALITY = bidict(
    window=QtCore.Qt.WindowModal,
    application=QtCore.Qt.ApplicationModal,
    none=QtCore.Qt.NonModal,
)

ModalityStr = Literal["window", "application", "none"]

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

FOCUS_POLICY = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

FocusPolicyStr = Literal["tab", "click", "strong", "wheel", "none"]

WINDOW_FLAGS = bidict(
    frameless=QtCore.Qt.FramelessWindowHint,
    popup=QtCore.Qt.Popup,
    stay_on_top=QtCore.Qt.WindowStaysOnTopHint,
    tool=QtCore.Qt.Tool,
    window_title=QtCore.Qt.WindowTitleHint,
    customize_window=QtCore.Qt.CustomizeWindowHint,
)

ATTRIBUTES = bidict(
    native_window=QtCore.Qt.WA_NativeWindow,
    no_native_ancestors=QtCore.Qt.WA_DontCreateNativeAncestors,
)

WINDOW_STATES = bidict(
    none=QtCore.Qt.WindowNoState,
    minimized=QtCore.Qt.WindowMinimized,
    maximized=QtCore.Qt.WindowMaximized,
    fullscreen=QtCore.Qt.WindowFullScreen,
    active=QtCore.Qt.WindowActive,
)

WindowStateStr = Literal["none", "minimized", "maximized", "fullscreen", "active"]

QtWidgets.QWidget.__bases__ = (core.Object, QtGui.QPaintDevice)


class Widget(prettyprinter.PrettyPrinter, QtWidgets.QWidget):
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        params = helpers.format_kwargs(self.serialize_fields())
        return f"{cls_name}({params})"

    def __setstate__(self, state: Dict[str, Any]) -> None:
        if self.layout() is None:
            self.set_layout(state["layout"])
        self.setSizePolicy(state["size_policy"])
        self.setAccessibleName(state["accessible_name"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self) -> Dict[str, Any]:
        icon = gui.Icon(self.windowIcon())
        return dict(
            layout=self.layout() if isinstance(self.layout(), widgets.Layout) else None,
            size_policy=self.get_size_policy(),
            actions=self.actions(),
            accessible_name=self.accessibleName(),
            tool_tip=self.toolTip(),
            tooltip_duration=self.toolTipDuration(),
            window_title=self.windowTitle(),
            enabled=self.isEnabled(),
            visible=self.isVisible(),
            stylesheet=self.styleSheet(),
            icon=icon if not icon.isNull() else None,
            modality=self.get_modality(),
            whats_this=self.whatsThis(),
            contextmenu_policy=self.get_contextmenu_policy(),
            focus_policy=self.get_focus_policy(),
            status_tip=self.statusTip(),
        )

    def resize(self, *size) -> None:
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_icon(self, icon: gui.icon.IconType) -> None:
        """Set the window icon.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def set_min_size(self, *size) -> None:
        self.setMinimumSize(*size)

    def set_max_size(self, *size) -> None:
        self.setMaximumSize(*size)

    def set_min_width(self, width: Optional[int]) -> None:
        if width is None:
            width = 0
        self.setMinimumWidth(width)

    def set_max_width(self, width: Optional[int]) -> None:
        if width is None:
            width = QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumWidth(width)

    def set_min_height(self, height: Optional[int]) -> None:
        if height is None:
            height = 0
        self.setMinimumHeight(height)

    def set_max_height(self, height: Optional[int]) -> None:
        if height is None:
            height = QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumHeight(height)

    @property
    def title(self) -> str:
        return self.windowTitle()

    @title.setter
    def title(self, name: str):
        self.setWindowTitle(name)

    @property
    def enabled(self) -> bool:
        return self.isEnabled()

    @enabled.setter
    def enabled(self, state: bool):
        self.setEnabled(state)

    def set_enabled(self, enabled: bool = True) -> None:
        self.setEnabled(enabled)

    def set_disabled(self) -> None:
        self.setEnabled(False)

    def set_title(self, title: str) -> None:
        self.setWindowTitle(title)

    def get_title(self) -> str:
        return self.windowTitle()

    def set_tooltip(self, text: str) -> None:
        self.setToolTip(text)

    def set_font(
        self,
        font_name: Optional[str] = None,
        font_size: int = -1,
        weight: int = -1,
        italic: bool = False,
    ) -> gui.Font:
        if font_name is None:
            font_name = self.font().family()
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)
        return font

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def set_window_flags(self, *flags: str, append: bool = False):
        for flag in flags:
            if flag not in WINDOW_FLAGS:
                raise InvalidParamError(flag, WINDOW_FLAGS)
        result = helpers.merge_flags(flags, WINDOW_FLAGS)
        if append:
            result = result | self.windowFlags()
        self.setWindowFlags(result)

    def set_flags(
        self,
        minimize: Optional[bool] = None,
        maximize: Optional[bool] = None,
        close: Optional[bool] = None,
        stay_on_top: Optional[bool] = None,
        frameless: Optional[bool] = None,
        window: Optional[bool] = None,
    ) -> None:
        if minimize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, minimize)
        if maximize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, maximize)
        if close is not None:
            self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, close)
        if stay_on_top is not None:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, stay_on_top)
        if frameless is not None:
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint, frameless)
        if window is not None:
            self.setWindowFlag(QtCore.Qt.Window, window)

    def set_attribute(self, attribute: str, state: bool = True) -> None:
        if attribute not in ATTRIBUTES:
            raise InvalidParamError(attribute, ATTRIBUTES)
        self.setAttribute(ATTRIBUTES[attribute], state)

    def set_attributes(self, **kwargs: Dict[str, bool]) -> None:
        for attribute, state in kwargs.items():
            if attribute not in ATTRIBUTES:
                raise InvalidParamError(attribute, ATTRIBUTES)
            self.setAttribute(ATTRIBUTES[attribute], state)

    def set_modality(self, modality: ModalityStr) -> None:
        """Set modality for the dialog.

        Args:
            modality: modality for the main window

        Raises:
            InvalidParamError: modality type does not exist
        """
        if modality not in MODALITY:
            raise InvalidParamError(modality, MODALITY)
        self.setWindowModality(MODALITY[modality])

    def get_modality(self) -> ModalityStr:
        """Get the current modality modes as a string.

        Returns:
            modality mode
        """
        return MODALITY.inverse[self.windowModality()]

    def set_size_policy(
        self,
        horizontal: Optional[widgets.sizepolicy.SizePolicyStr] = None,
        vertical: Optional[widgets.sizepolicy.SizePolicyStr] = None,
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
        pol = widgets.SizePolicy(
            qpol.horizontalPolicy(), qpol.verticalPolicy(), qpol.controlType()
        )
        pol.setHeightForWidth(qpol.hasHeightForWidth())
        pol.setWidthForHeight(qpol.hasWidthForHeight())
        pol.setHorizontalStretch(qpol.horizontalStretch())
        pol.setVerticalStretch(qpol.verticalStretch())
        return pol

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def set_background_color(self, color: colors.ColorType) -> None:
        col_str = "" if color is None else colors.get_color(color).name()
        with self.edit_stylesheet() as ss:
            ss.backgroundColor.setValue(col_str)

    @contextmanager
    def updates_off(self) -> Iterator[None]:
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(True)

    @contextmanager
    def edit_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        ss = qstylizer.parser.parse(self.styleSheet())
        yield ss
        self.setStyleSheet(ss.toString())

    @contextmanager
    def edit_palette(self) -> Iterator[gui.Palette]:
        palette = gui.Palette(self.palette())
        yield palette
        self.setPalette(palette)

    @contextmanager
    def edit_font(self) -> Iterator[gui.Font]:
        font = gui.Font(self.font())
        yield font
        self.setFont(font)

    @deprecated(reason="This context manager is deprecated, use edit_font instead.")
    @contextmanager
    def current_font(self) -> Iterator[gui.Font]:
        with self.edit_font() as font:
            yield font

    def set_contextmenu_policy(self, policy: ContextPolicyStr) -> None:
        """Set contextmenu policy for given item view.

        Args:
            policy: contextmenu policy to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in CONTEXT_POLICY:
            raise InvalidParamError(policy, CONTEXT_POLICY)
        self.setContextMenuPolicy(CONTEXT_POLICY[policy])

    def get_contextmenu_policy(self) -> ContextPolicyStr:
        """Return current contextmenu policy.

        Returns:
            contextmenu policy
        """
        return CONTEXT_POLICY.inverse[self.contextMenuPolicy()]

    def set_window_state(self, policy: WindowStateStr) -> None:
        """Set window state for given item view.

        Args:
            policy: window state to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in WINDOW_STATES:
            raise InvalidParamError(policy, WINDOW_STATES)
        self.setWindowState(WINDOW_STATES[policy])

    def get_window_state(self) -> WindowStateStr:
        """Return current window state.

        Returns:
            window state
        """
        return WINDOW_STATES.inverse[self.windowState()]

    def set_custom_menu(self, method: Callable) -> None:
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(
        self,
        layout: Union[str, QtWidgets.QLayout, None],
        margin: Optional[int] = None,
        spacing: Optional[int] = None,
    ) -> None:
        if layout is None:
            return None
        if layout in ["horizontal", "vertical"]:
            self.box = widgets.BoxLayout(layout)
        elif layout == "grid":
            self.box = widgets.GridLayout()
        elif layout == "form":
            self.box = widgets.FormLayout()
        elif layout == "stacked":
            self.box = widgets.StackedLayout()
        elif layout == "flow":
            from prettyqt import custom_widgets

            self.box = custom_widgets.FlowLayout()
        elif isinstance(layout, QtWidgets.QLayout):
            self.box = layout
        else:
            raise ValueError("Invalid Layout")
        self.setLayout(self.box)
        if margin is not None:
            self.box.set_margin(margin)
        if spacing is not None:
            self.box.setSpacing(spacing)

    def center(self) -> None:
        qr = self.frameGeometry()
        cp = gui.GuiApplication.screens()[0].geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_cursor(self, cursor: CursorShapeStr) -> None:
        if cursor not in CURSOR_SHAPE:
            raise InvalidParamError(cursor, CURSOR_SHAPE)
        self.setCursor(CURSOR_SHAPE[cursor])

    def set_focus_policy(self, policy: FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy (str): Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in FOCUS_POLICY:
            raise InvalidParamError(policy, FOCUS_POLICY)
        self.setFocusPolicy(FOCUS_POLICY[policy])

    def get_focus_policy(self) -> FocusPolicyStr:
        """Return waay the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return FOCUS_POLICY.inverse[self.focusPolicy()]

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
        x: int,
        y: int,
        width: int,
        height: int,
        typ: gui.region.RegionTypeStr = "rectangle",
    ):
        self.setMask(gui.Region(x, y, width, height, gui.region.REGION_TYPE[typ]))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.main_loop()
