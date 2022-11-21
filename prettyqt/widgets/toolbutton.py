from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


POPUP_MODE = bidict(
    delayed=QtWidgets.QToolButton.ToolButtonPopupMode.DelayedPopup,
    menu_button=QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup,
    instant=QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup,
)

PopupModeStr = Literal["delayed", "menu_button", "instant"]


QtWidgets.QToolButton.__bases__ = (widgets.AbstractButton,)


class ToolButton(QtWidgets.QToolButton):
    def __getitem__(self, item: str) -> QtWidgets.QAction:
        menu = self.menu()
        return menu[item]

    # def set_menu(self, menu: QtWidgets.QMenu):
    #     menu.setParent(self)
    #     self.setMenu(menu)

    @classmethod
    def for_menu(cls, menu: QtWidgets.QMenu, icon: types.IconType = None):
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

    def set_arrow_type(self, mode: constants.ArrowTypeStr):
        """Set the arrow type of the toolbutton.

        Args:
            mode: arrow type to use

        Raises:
            InvalidParamError: invalid arrow type
        """
        if mode not in constants.ARROW_TYPE:
            raise InvalidParamError(mode, constants.ARROW_TYPE)
        self.setArrowType(constants.ARROW_TYPE[mode])

    def get_arrow_type(self) -> constants.ArrowTypeStr:
        """Return arrow type.

        Returns:
            arrow type
        """
        return constants.ARROW_TYPE.inverse[self.arrowType()]

    def set_style(self, style: constants.ToolButtonStyleStr):
        """Set the toolbutton style.

        Args:
            style: style to use

        Raises:
            InvalidParamError: invalid style
        """
        if style not in constants.TOOLBUTTON_STYLE:
            raise InvalidParamError(style, constants.TOOLBUTTON_STYLE)
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE[style])

    def get_style(self) -> constants.ToolButtonStyleStr:
        """Return toolbutton style.

        Returns:
            toolbutton style
        """
        return constants.TOOLBUTTON_STYLE.inverse[self.toolButtonStyle()]


if __name__ == "__main__":
    app = widgets.app()
    w = ToolButton()
    # icon = gui.Icon()
    # icon.add_pixmap("mdi.timer")
    # icon.add_pixmap("mdi.folder", state="on")
    w.set_icon("mdi.timer", "mdi.folder")
    w.show()
    app.main_loop()
