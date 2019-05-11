# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import functools
from typing import Callable, Iterable, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets

POLICIES = dict(custom=QtCore.Qt.CustomContextMenu,
                showhide_menu="showhide_menu")


class HeaderView(QtWidgets.QHeaderView):
    MODES = dict(interactive=QtWidgets.QHeaderView.Interactive,
                 fixed=QtWidgets.QHeaderView.Fixed,
                 stretch=QtWidgets.QHeaderView.Stretch,
                 resize_to_contents=QtWidgets.QHeaderView.ResizeToContents)

    section_vis_changed = QtCore.Signal(int, bool)

    def __init__(self, parent):
        super().__init__(QtCore.Qt.Horizontal, parent=parent)
        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self.widget_name = parent.objectName()

    def save_state(self):
        settings = core.Settings()
        settings.setValue(f"{self.widget_name}.state", self.saveState())

    def load_state(self):
        settings = core.Settings()
        state = settings.value(f"{self.widget_name}.state", None)
        if state is not None:
            self.restoreState(state)

    def resize_sections(self, mode: str):
        self.resizeSections(self.MODES[mode])

    def resize_mode(self, mode: str, col: Optional[int] = None):
        if mode not in self.MODES:
            raise ValueError("mode not existing")
        if col is None:
            self.setSectionResizeMode(self.MODES[mode])
        else:
            self.setSectionResizeMode(col, self.MODES[mode])

    def section_labels(self):
        model = self.parent().model()
        return [model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
                for i in range(self.count())]

    def set_contextmenu_policy(self, policy):
        self.setContextMenuPolicy(POLICIES[policy])

    def contextMenuEvent(self, event):
        """
        context menu for our files tree
        """
        menu = widgets.Menu(parent=self)
        for i, header_label in enumerate(self.section_labels()[1:], start=1):
            act = menu.addAction(header_label)
            act.setCheckable(True)
            val = not self.isSectionHidden(i)
            act.setChecked(val)
            fn = functools.partial(self.change_section_vis, i=i, val=val)
            act.triggered.connect(fn)
        menu.exec_(self.mapToGlobal(event.pos()))

    def set_custom_menu(self, method: Callable):
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def change_section_vis(self, i, val):
        self.section_vis_changed.emit(i, val)
        self.setSectionHidden(i, val)

    def set_sizes(self, sizes: Iterable):
        for i, size in enumerate(sizes):
            if size is not None:
                self.resizeSection(i, size)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    header = HeaderView(parent=None)
    app.exec_()
