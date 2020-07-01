# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Callable, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, icons


STYLES = bidict(icon=QtCore.Qt.ToolButtonIconOnly,
                text=QtCore.Qt.ToolButtonTextOnly,
                text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
                text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon)

TOOLBAR_AREAS = bidict(left=QtCore.Qt.LeftToolBarArea,
                       right=QtCore.Qt.RightToolBarArea,
                       top=QtCore.Qt.TopToolBarArea,
                       bottom=QtCore.Qt.BottomToolBarArea,
                       all=QtCore.Qt.AllToolBarAreas,
                       none=QtCore.Qt.NoToolBarArea)


QtWidgets.QToolBar.__bases__ = (widgets.Widget,)


class ToolBar(QtWidgets.QToolBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self.menu_buttons = list()

    def add_menu_button(self,
                        label: str,
                        icon: icons.IconType,
                        menu: QtWidgets.QMenu) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu)
        btn.setText(label)
        btn.setToolButtonStyle(self.toolButtonStyle())
        btn.set_icon(icon)
        self.menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def add_separator(self, text: Optional[str] = None, before: QtWidgets.QAction = None):
        """adds a separator showing an optional label

        Args:
            text: Text to show on separator
            before: insert separator before specific action

        Returns:
            Separator action
        """
        if text is None:
            if before:
                self.insertSeparator(before)
            else:
                self.addSeparator()
        else:
            label = widgets.Label(text)
            label.setMinimumWidth(self.minimumWidth())
            label.setStyleSheet("background:lightgrey")
            label.set_alignment(horizontal="center")
            if before:
                self.insertWidget(before, label)
            else:
                self.addWidget(label)

    def set_style(self, style: str):
        if style is None:
            return None
        self.setToolButtonStyle(STYLES[style])
        for btn in self.menu_buttons:
            btn.set_style(style)

    def get_style(self) -> str:
        """returns current style

        Possible values: "icon", "text", "text_below_icon", "text_beside_icon"

        Returns:
            style
        """
        return STYLES.inv[self.toolButtonStyle()]

    def add_action(self,
                   label: str,
                   icon: icons.IconType = None,
                   callback: Optional[Callable] = None,
                   checkable: bool = False):
        icon = icons.get_icon(icon)
        action = self.addAction(icon, label)
        if callback is not None:
            action.triggered.connect(callback)
        if checkable:
            action.setCheckable(True)
        return action

    def add_spacer(self):
        spacer = widgets.Widget()
        spacer.set_size_policy("expanding", "expanding")
        return self.addWidget(spacer)

    def set_icon_size(self, size: int):
        self.setIconSize(core.Size(size, size))

    def set_font_size(self, size: int):
        self.setStyleSheet(f"font-size: {size}pt;")

    def is_area_allowed(self, area: str):
        """check if toolbar is allowed at specified area

        Valid values for area: "left", "right", "top", "bottom"

        Args:
            area: area of the toolbar

        Raises:
            ValueError: area does not exist
        """
        if area not in TOOLBAR_AREAS:
            raise ValueError("Area not existing")
        return self.isAreaAllowed(TOOLBAR_AREAS[area])

    def set_allowed_areas(self, areas):
        self.setAllowedAreas(TOOLBAR_AREAS[areas])


if __name__ == "__main__":
    app = widgets.app()
    widget = ToolBar()
    widget.show()
    app.exec_()
