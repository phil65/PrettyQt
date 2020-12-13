from typing import Literal

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets
from prettyqt.utils import bidict, InvalidParamError


POPUP_MODE = bidict(
    delayed=QtWidgets.QToolButton.DelayedPopup,
    menu_button=QtWidgets.QToolButton.MenuButtonPopup,
    instant=QtWidgets.QToolButton.InstantPopup,
)

PopupModeStr = Literal["delayed", "menu_button", "instant"]

ARROW_TYPE = bidict(
    none=QtCore.Qt.NoArrow,
    up=QtCore.Qt.UpArrow,
    down=QtCore.Qt.DownArrow,
    left=QtCore.Qt.LeftArrow,
    right=QtCore.Qt.RightArrow,
)

ArrowTypeStr = Literal["none", "up", "down", "left", "right"]

STYLE = bidict(
    icon=QtCore.Qt.ToolButtonIconOnly,
    text=QtCore.Qt.ToolButtonTextOnly,
    text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
    text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon,
)

StyleStr = Literal["icon", "text", "text_beside_icon", "text_below_icon"]


QtWidgets.QToolButton.__bases__ = (widgets.AbstractButton,)


class ToolButton(QtWidgets.QToolButton):
    def __getitem__(self, item: str) -> QtWidgets.QAction:
        menu = self.menu()
        return menu[item]

    @classmethod
    def for_menu(cls, menu: QtWidgets.QMenu, icon: gui.icon.IconType = None):
        btn = cls()
        btn.setMenu(menu)
        # btn.set_title(menu.title())
        btn.set_popup_mode("instant")
        btn.set_icon(icon)
        return btn

    def set_default_action(self, action):
        self.setDefaultAction(action)

    def set_popup_mode(self, mode: PopupModeStr):
        """Set the popup mode of the toolbutton.

        Args:
            mode: popup mode to use

        Raises:
            InvalidParamError: invalid popup mode
        """
        if mode not in POPUP_MODE:
            raise InvalidParamError(mode, POPUP_MODE)
        self.setPopupMode(POPUP_MODE[mode])

    def get_popup_mode(self) -> PopupModeStr:
        """Return popup mode.

        Returns:
            popup mode
        """
        return POPUP_MODE.inverse[self.popupMode()]

    def set_arrow_type(self, mode: ArrowTypeStr):
        """Set the arrow type of the toolbutton.

        Args:
            mode: arrow type to use

        Raises:
            InvalidParamError: invalid arrow type
        """
        if mode not in ARROW_TYPE:
            raise InvalidParamError(mode, ARROW_TYPE)
        self.setArrowType(ARROW_TYPE[mode])

    def get_arrow_type(self) -> ArrowTypeStr:
        """Return arrow type.

        Returns:
            arrow type
        """
        return ARROW_TYPE.inverse[self.arrowType()]

    def set_style(self, style: StyleStr):
        """Set the toolbutton style.

        Args:
            style: style to use

        Raises:
            InvalidParamError: invalid style
        """
        if style not in STYLE:
            raise InvalidParamError(style, STYLE)
        self.setToolButtonStyle(STYLE[style])

    def get_style(self) -> StyleStr:
        """Return toolbutton style.

        Returns:
            toolbutton style
        """
        return STYLE.inverse[self.toolButtonStyle()]


if __name__ == "__main__":
    app = widgets.app()
    w = ToolButton()
