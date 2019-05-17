# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Union

import qtawesome as qta
from qtpy import QtWidgets, QtGui

from prettyqt import core, widgets, gui


class AbstractButton(QtWidgets.QAbstractButton):

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__getstate__()}"

    def __getstate__(self):
        return dict(object_name=self.objectName(),
                    text=self.text(),
                    icon=gui.Icon(self.icon()),
                    checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state["text"])
        self.setObjectName(state.get("object_name", ""))
        self.set_icon(state["icon"])
        self.setEnabled(state.get("enabled", True))
        self.setChecked(state.get("checked", False))
        self.setCheckable(state["checkable"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))

    def set_icon(self, icon: Union[QtGui.QIcon, str, None]):
        """set the icon for the button

        Args:
            icon: icon to use
        """
        if icon is None:
            icon = gui.Icon()
        elif isinstance(icon, str):
            icon = qta.icon(icon)
        self.setIcon(icon)

    def set_style_icon(self, icon: str, size: int = 15):
        STYLES = dict(close=QtWidgets.QStyle.SP_TitleBarCloseButton,
                      maximise=QtWidgets.QStyle.SP_TitleBarMaxButton)
        qicon = self.style().standardIcon(STYLES[icon], None, self)
        self.setIcon(qicon)
        self.setIconSize(core.Size(size, size))

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)


AbstractButton.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractButton()
    widget.show()
    app.exec_()
