# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable

import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets

STYLES = dict(icon=QtCore.Qt.ToolButtonIconOnly,
              text=QtCore.Qt.ToolButtonTextOnly,
              text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
              text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon)


class ToolBar(QtWidgets.QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self.menu_buttons = list()

    def add_menu_button(self,
                        label: str,
                        icon,
                        menu: QtWidgets.QMenu) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu)
        btn.setText(label)
        btn.setToolButtonStyle(self.toolButtonStyle())
        btn.set_icon(icon)
        self.menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def set_style(self, style: str):
        if style is None:
            return None
        self.setToolButtonStyle(STYLES.get(style, 0))
        for btn in self.menu_buttons:
            btn.setToolButtonStyle(STYLES.get(style, 0))

    def add_action(self, label: str, icon, callback: Callable, checkable=False):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        action = self.addAction(icon, label, callback)
        if checkable:
            action.setCheckable(True)
        return action

    def set_icon_size(self, size: int):
        self.setIconSize(core.Size(size, size))

    def set_font_size(self, size: int):
        self.setStyleSheet(f"font-size: {size}pt;")


ToolBar.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    widget = ToolBar()
    widget.show()
    app.exec_()
