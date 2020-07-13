# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import bidict


POPUP_MODES = bidict(
    delayed=QtWidgets.QToolButton.DelayedPopup,
    menu_button=QtWidgets.QToolButton.MenuButtonPopup,
    instant=QtWidgets.QToolButton.InstantPopup,
)

ARROW_TYPES = bidict(
    none=QtCore.Qt.NoArrow,
    up=QtCore.Qt.UpArrow,
    down=QtCore.Qt.DownArrow,
    left=QtCore.Qt.LeftArrow,
    right=QtCore.Qt.RightArrow,
)

STYLES = bidict(
    icon=QtCore.Qt.ToolButtonIconOnly,
    text=QtCore.Qt.ToolButtonTextOnly,
    text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
    text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon,
)

QtWidgets.QToolButton.__bases__ = (widgets.AbstractButton,)


class ToolButton(QtWidgets.QToolButton):
    def __getitem__(self, item):
        menu = self.menu()
        return menu[item]

    @classmethod
    def for_menu(cls, menu: QtWidgets.QMenu, icon: gui.icon.IconType = None):
        btn = cls()
        btn.setMenu(menu)
        btn.set_popup_mode("instant")
        btn.set_icon(icon)
        return btn

    def set_default_action(self, action):
        self.setDefaultAction(action)

    def set_popup_mode(self, mode: str):
        """sets the popup mode of the toolbutton

        valid values are: "delayed", "menu_button", "instant"

        Args:
            mode: popup mode to use

        Raises:
            ValueError: invalid popup mode
        """
        if mode not in POPUP_MODES:
            raise ValueError("Invalid mode.")
        self.setPopupMode(POPUP_MODES[mode])

    def get_popup_mode(self) -> str:
        """returns popup mode

        possible values are "delayed", "menu_button", "instant"

        Returns:
            popup mode
        """
        return POPUP_MODES.inv[self.popupMode()]

    def set_arrow_type(self, mode: str):
        """sets the arrow type of the toolbutton

        valid values are: "none", "up", "down", "left", "right"

        Args:
            mode: arrow type to use

        Raises:
            ValueError: invalid arrow type
        """
        if mode not in ARROW_TYPES:
            raise ValueError("Invalid arrow type.")
        self.setArrowType(ARROW_TYPES[mode])

    def get_arrow_type(self) -> str:
        """returns arrow type

        possible values are "none", "up", "down", "left", "right"

        Returns:
            arrow type
        """
        return ARROW_TYPES.inv[self.arrowType()]

    def set_style(self, style: str):
        if style not in STYLES:
            raise ValueError("Invalid style.")
        self.setToolButtonStyle(STYLES[style])


if __name__ == "__main__":
    w = ToolButton()
