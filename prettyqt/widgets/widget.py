# -*- coding: utf-8 -*-
"""
"""

from contextlib import contextmanager
import functools
import operator
from typing import Callable, Optional, Union

from qtpy import QtCore, QtGui, QtWidgets
import qstylizer.parser

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, colors


CONTEXT_POLICIES = bidict(
    none=QtCore.Qt.NoContextMenu,
    prevent=QtCore.Qt.PreventContextMenu,
    default=QtCore.Qt.DefaultContextMenu,
    actions=QtCore.Qt.ActionsContextMenu,
    custom=QtCore.Qt.CustomContextMenu,
    # showhide_menu="showhide_menu",
)

MODALITIES = bidict(
    window=QtCore.Qt.WindowModal,
    application=QtCore.Qt.ApplicationModal,
    none=QtCore.Qt.NonModal,
)

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

FOCUS_POLICIES = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

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

QtWidgets.QWidget.__bases__ = (core.Object, QtGui.QPaintDevice)


class Widget(QtWidgets.QWidget):
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__getstate__()}"

    def __getstate__(self):
        return dict(
            layout=self.layout(),
            size_policy=self.get_size_policy(),
            accessible_name=self.accessibleName(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_layout(state["layout"])
        self.setSizePolicy(state["size_policy"])
        self.setAccessibleName(state["accessible_name"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

    def resize(self, *size):
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_icon(self, icon: gui.icon.IconType):
        """set the window icon

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def set_min_size(self, *size):
        self.setMinimumSize(*size)

    def set_max_size(self, *size):
        self.setMaximumSize(*size)

    def set_min_width(self, width: Optional[int]):
        if width is None:
            width = 0
        self.setMinimumWidth(width)

    def set_max_width(self, width: Optional[int]):
        if width is None:
            width = QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumWidth(width)

    def set_min_height(self, height: Optional[int]):
        if height is None:
            height = 0
        self.setMinimumHeight(height)

    def set_max_height(self, height: Optional[int]):
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

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_disabled(self):
        self.setEnabled(False)

    def set_title(self, title: str):
        self.setWindowTitle(title)

    def set_tooltip(self, text: str):
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

    def set_window_flags(self, *flags: str, append: bool = False):
        for flag in flags:
            if flag not in WINDOW_FLAGS:
                raise ValueError("Invalid window flag")
        flags = functools.reduce(operator.ior, [WINDOW_FLAGS[t] for t in flags])
        if append:
            flags = flags | self.windowFlags()
        self.setWindowFlags(flags)

    def set_flags(
        self,
        minimize: Optional[bool] = None,
        maximize: Optional[bool] = None,
        close: Optional[bool] = None,
        stay_on_top: Optional[bool] = None,
        frameless: Optional[bool] = None,
        window: Optional[bool] = None,
    ):
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

    def set_attribute(self, attribute: str, state: bool = True):
        if attribute not in ATTRIBUTES:
            raise ValueError(f"Invalid attribute '{attribute}'.")
        self.setAttribute(ATTRIBUTES[attribute], state)

    def set_modality(self, modality: str = "window"):
        """set modality for the dialog

        Valid values for modality: "none", "window", "application"

        Args:
            modality: modality for the main window

        Raises:
            ValueError: modality type does not exist
        """
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])

    def get_modality(self) -> str:
        """get the current modality modes as a string

        Possible values: "none", "window", "application"

        Returns:
            modality mode
            str
        """
        return MODALITIES.inv[self.windowModality()]

    def set_size_policy(
        self, horizontal: Optional[str] = None, vertical: Optional[str] = None
    ):
        """sets the sizes policy

        possible values for both parameters are "fixed", "minimum", "maximum",
        "preferred", "expanding", "minimum_expanding" and "ignored"

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

    def get_size_policy(self):
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

    def set_background_color(self, color: colors.ColorType):
        col_str = "" if color is None else colors.get_color(color).name()
        with self.edit_stylesheet() as ss:
            ss.backgroundColor.setValue(col_str)

    @contextmanager
    def updates_off(self):
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(True)

    @contextmanager
    def edit_stylesheet(self):
        ss = qstylizer.parser.parse(self.styleSheet())
        yield ss
        self.setStyleSheet(ss.toString())

    @contextmanager
    def current_font(self):
        font = gui.Font(self.font())
        yield font
        self.setFont(font)

    def set_contextmenu_policy(self, policy: str):
        """set contextmenu policy for given item view

        Allowed values are "none", "prevent", "default", "actions", "custom"

        Args:
            policy: contextmenu policy to use

        Raises:
            ValueError: policy does not exist
        """
        if policy not in CONTEXT_POLICIES:
            raise ValueError("invalid selection behaviour")
        self.setContextMenuPolicy(CONTEXT_POLICIES[policy])

    def get_contextmenu_policy(self) -> str:
        """returns current contextmenu policy

        Possible values: "none", "prevent", "default", "actions", "custom"

        Returns:
            contextmenu policy
        """
        return CONTEXT_POLICIES.inv[self.contextMenuPolicy()]

    def set_custom_menu(self, method: Callable):
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(
        self, layout: Union[str, QtWidgets.QLayout, None], margin: Optional[int] = None
    ):
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
            self.box.setContentsMargins(margin, margin, margin, margin)

    def center(self):
        qr = self.frameGeometry()
        cp = gui.GuiApplication.screens()[0].geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_cursor(self, cursor: str):
        if cursor not in CURSOR_SHAPES:
            raise ValueError(
                f"Invalid cursor '{cursor}'. " f"Valid values: {CURSOR_SHAPES.keys()}"
            )
        self.setCursor(CURSOR_SHAPES[cursor])

    def set_focus_policy(self, policy: str):
        if policy not in FOCUS_POLICIES:
            raise ValueError(
                f"Invalid policy '{policy}'. " f"Valid values: {FOCUS_POLICIES.keys()}"
            )
        self.setFocusPolicy(FOCUS_POLICIES[policy])

    def get_focus_policy(self) -> str:
        return FOCUS_POLICIES.inv[self.focusPolicy()]

    def set_font_size(self, size: int):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    def font_metrics(self):
        return gui.FontMetrics(self.fontMetrics())

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()
