# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import core, widgets, gui


class CommandLinkButton(QtWidgets.QCommandLinkButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def __repr__(self):
        return f"CommandLinkButton: {self.__getstate__()}"

    def __getstate__(self):
        return dict(object_name=self.objectName(),
                    title=self.text(),
                    icon=gui.Icon(self.icon()),
                    description=self.description(),
                    checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        self.__init__(state["title"])
        self.setObjectName(state["object_name"])
        self.setDescription(state["description"])
        self.set_icon(state["icon"])
        self.setEnabled(state["enabled"])
        self.setChecked(state["checked"])
        self.setCheckable(state["checkable"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_style_icon(self, icon: str, size: int = 15):
        STYLES = dict(close=QtWidgets.QStyle.SP_TitleBarCloseButton,
                      maximise=QtWidgets.QStyle.SP_TitleBarMaxButton)
        qicon = self.style().standardIcon(STYLES[icon], None, self)
        self.setIcon(qicon)
        self.setIconSize(core.Size(size, size))


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = CommandLinkButton("This is a test")
    widget.show()
    app.exec_()
