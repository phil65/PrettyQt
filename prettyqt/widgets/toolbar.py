# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable, Optional

from qtpy import QtWidgets, QtCore
import qtawesome as qta

from prettyqt import widgets, core

STYLES = dict(icon=QtCore.Qt.ToolButtonIconOnly,
              text=QtCore.Qt.ToolButtonTextOnly,
              text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
              text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon)


class Toolbar(QtWidgets.QToolBar):

    ICON_SIZE = 20

    def __init__(self, *args, **kwargs):
        self.menu_buttons = list()
        super().__init__(*args, **kwargs)
        self.set_icon_size(self.ICON_SIZE)

    def add_menu_button(self,
                        label: str,
                        icon,
                        menu: QtWidgets.QMenu,
                        style: Optional[str] = None) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu)
        btn.setText(label)
        if style:
            btn.setToolButtonStyle(STYLES.get(style, "text_below_icon"))
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


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = Toolbar()
    widget.show()
    app.exec_()
