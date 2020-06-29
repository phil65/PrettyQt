# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from contextlib import contextmanager
from typing import Callable, Dict, Optional

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict

POLICIES = bidict(none=QtCore.Qt.NoContextMenu,
                  prevent=QtCore.Qt.PreventContextMenu,
                  default=QtCore.Qt.DefaultContextMenu,
                  actions=QtCore.Qt.ActionsContextMenu,
                  custom=QtCore.Qt.CustomContextMenu,
                  showhide_menu="showhide_menu")

MODALITIES = bidict(window=QtCore.Qt.WindowModal,
                    application=QtCore.Qt.ApplicationModal,
                    none=QtCore.Qt.NonModal)

CURSOR_SHAPES = bidict(arrow=QtCore.Qt.ArrowCursor,
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
                       bitmap=QtCore.Qt.BitmapCursor)

FOCUS_POLICIES = bidict(tab=QtCore.Qt.TabFocus,
                        click=QtCore.Qt.ClickFocus,
                        strong=QtCore.Qt.StrongFocus,
                        wheel=QtCore.Qt.WheelFocus,
                        none=QtCore.Qt.NoFocus)

QtWidgets.QWidget.__bases__ = (core.Object, QtGui.QPaintDevice)


class Widget(QtWidgets.QWidget):

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__getstate__()}"

    def __getstate__(self):
        return dict(layout=self.layout(),
                    size_policy=self.get_size_policy(),
                    accessible_name=self.accessibleName(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip())

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

    def set_min_size(self, *size):
        self.setMinimumSize(*size)

    def set_max_size(self, *size):
        self.setMaximumSize(*size)

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

    def set_font(self,
                 font_name: Optional[str] = None,
                 font_size: int = -1,
                 weight: int = -1,
                 italic: bool = False) -> gui.Font:
        if font_name is None:
            font_name = self.font().family()
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)
        return font

    def set_modality(self, modality: str = "window"):
        """set modality for the dialog

        Valid values for modality: "modeless", "window", "application"

        Args:
            modality: modality for the main window (default: {"window"})

        Raises:
            ValueError: modality type does not exist
        """
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])

    def get_modality(self) -> str:
        """get the current modality modes as a string

        Possible values: "modeless", "window", "application"

        Returns:
            modality mode
            str
        """
        return MODALITIES.inv[self.windowModality()]

    @contextmanager
    def updates_off(self):
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(True)

    def set_size_policy(self,
                        horizontal: Optional[str] = None,
                        vertical: Optional[str] = None):
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
        pol = widgets.SizePolicy(qpol.horizontalPolicy(),
                                 qpol.verticalPolicy(),
                                 qpol.controlType())
        pol.setHeightForWidth(qpol.hasHeightForWidth())
        pol.setWidthForHeight(qpol.hasWidthForHeight())
        pol.setHorizontalStretch(qpol.horizontalStretch())
        pol.setVerticalStretch(qpol.verticalStretch())
        return pol

    def set_background_color(self, color):
        self.setStyleSheet(f"background-color: {color};")

    def set_stylesheet(self, item, dct: Dict[str, str]) -> str:
        ss = "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in dct.items())
        stylesheet = f"{item} {{{ss};}}"
        self.setStyleSheet(stylesheet)
        return stylesheet

    def set_contextmenu_policy(self, policy: str):
        """set contextmenu policy for given item view

        Allowed values are "none", "prevent", "default", "actions",
                           "custom", "showhide_menu"

        Args:
            policy: contextmenu policy to use

        Raises:
            ValueError: policy does not exist
        """
        if policy not in POLICIES:
            raise ValueError("invalid selection behaviour")
        self.setContextMenuPolicy(POLICIES[policy])

    def get_contextmenu_policy(self) -> str:
        """returns current contextmenu policy

        Possible values: "none", "prevent", "default", "actions",
                         "custom", "showhide_menu"

        Returns:
            contextmenu policy
        """
        return POLICIES.inv[self.contextMenuPolicy()]

    def set_custom_menu(self, method: Callable):
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(self, layout):
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
        else:
            self.box = layout
        if self.box is not None:
            self.setLayout(self.box)

    def center(self):
        qr = self.frameGeometry()
        cp = gui.GuiApplication.screens()[0].geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def raise_dock(self) -> bool:
        node = self
        while node:
            node = node.parent()
            if isinstance(node, QtWidgets.QDockWidget):
                node.setVisible(True)
                node.raise_()
                return True
        return False

    def set_cursor(self, cursor: str):
        if cursor not in CURSOR_SHAPES:
            raise ValueError(f"Invalid cursor '{cursor}'. "
                             f"Valid values: {CURSOR_SHAPES.keys()}")
        self.setCursor(CURSOR_SHAPES[cursor])

    def set_focus_policy(self, policy: str):
        if policy not in FOCUS_POLICIES:
            raise ValueError(f"Invalid policy '{policy}'. "
                             f"Valid values: {FOCUS_POLICIES.keys()}")
        self.setFocusPolicy(FOCUS_POLICIES[policy])

    def get_focus_policy(self) -> str:
        return FOCUS_POLICIES.inv[self.focusPolicy()]


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()
