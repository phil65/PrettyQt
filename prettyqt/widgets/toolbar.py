# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable

from qtpy import QtWidgets, QtCore
import qtawesome as qta

STYLES = {"icon": QtCore.Qt.ToolButtonIconOnly,
          "text": QtCore.Qt.ToolButtonTextOnly,
          "text_beside_icon": QtCore.Qt.ToolButtonTextBesideIcon,
          "text_below_icon": QtCore.Qt.ToolButtonTextUnderIcon}


class Toolbar(QtWidgets.QToolBar):
    """
    Customized Toolbar class
    """

    ICON_SIZE = 20

    def __init__(self, *args, **kwargs):
        self.menu_buttons = list()
        super().__init__(*args, **kwargs)
        self.set_icon_size(self.ICON_SIZE)

    def add_menu_button(self,
                        label: str,
                        icon,
                        menu: QtWidgets.QMenu,
                        style: str = None) -> QtWidgets.QToolButton:
        btn = QtWidgets.QToolButton()
        btn.setText(label)
        if style:
            btn.setToolButtonStyle(STYLES[style])
        btn.setMenu(menu)
        if isinstance(icon, str):
            icon = qta.icon(icon)
        btn.setIcon(icon)
        btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def set_style(self, style):
        if style is None:
            return None
        self.setToolButtonStyle(style)
        for btn in self.menu_buttons:
            self.setToolButtonStyle(style)

    def add_action(self, label: str, icon, callback: Callable, checkable=False):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        action = self.addAction(icon, label, callback)
        if checkable:
            action.setCheckable(True)
        return action

    def set_icon_size(self, size: int):
        self.setIconSize(QtCore.QSize(size, size))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Toolbar()
    widget.show()
    app.exec_()
