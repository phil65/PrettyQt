from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt import constants, widgets
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, datatypes


PopupModeStr = Literal["delayed", "menu_button", "instant"]

POPUP_MODE: bidict[PopupModeStr, widgets.QToolButton.ToolButtonPopupMode] = bidict(
    delayed=widgets.QToolButton.ToolButtonPopupMode.DelayedPopup,
    menu_button=widgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup,
    instant=widgets.QToolButton.ToolButtonPopupMode.InstantPopup,
)


class ToolButton(widgets.AbstractButtonMixin, widgets.QToolButton):
    """Quick-access button to commands or options, usually used inside a QToolBar."""

    def __getitem__(self, item: str) -> QtGui.QAction:
        menu = self.menu()
        return menu[item]

    # def set_menu(self, menu: widgets.QMenu):
    #     menu.setParent(self)
    #     self.setMenu(menu)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "toolButtonStyle": constants.TOOLBUTTON_STYLE,
            "arrowType": constants.ARROW_TYPE,
            "popupMode": POPUP_MODE,
        }
        return maps

    @classmethod
    def for_menu(cls, menu: widgets.QMenu, icon: datatypes.IconType = None) -> Self:
        btn = cls()
        btn.setMenu(menu)
        # btn.set_title(menu.title())
        btn.set_popup_mode("instant")
        btn.set_icon(icon)
        return btn

    def set_default_action(self, action: QtGui.QAction):
        self.setDefaultAction(action)

    def set_popup_mode(
        self, mode: PopupModeStr | widgets.QToolButton.ToolButtonPopupMode
    ):
        """Set the popup mode of the toolbutton.

        Args:
            mode: popup mode to use
        """
        self.setPopupMode(POPUP_MODE.get_enum_value(mode))

    def get_popup_mode(self) -> PopupModeStr:
        """Return popup mode.

        Returns:
            popup mode
        """
        return POPUP_MODE.inverse[self.popupMode()]

    def set_arrow_type(self, mode: constants.ArrowTypeStr | constants.ArrowType):
        """Set the arrow type of the toolbutton.

        Args:
            mode: arrow type to use
        """
        self.setArrowType(constants.ARROW_TYPE.get_enum_value(mode))

    def get_arrow_type(self) -> constants.ArrowTypeStr:
        """Return arrow type.

        Returns:
            arrow type
        """
        return constants.ARROW_TYPE.inverse[self.arrowType()]

    def set_style(self, style: constants.ToolButtonStyleStr | constants.ToolButtonStyle):
        """Set the toolbutton style.

        Args:
            style: style to use
        """
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE.get_enum_value(style))

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
    app.exec()
