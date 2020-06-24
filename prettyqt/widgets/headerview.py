# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import functools
from typing import Iterable, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict

QtWidgets.QHeaderView.__bases__ = (widgets.AbstractItemView,)


class HeaderView(QtWidgets.QHeaderView):
    MODES = bidict(interactive=QtWidgets.QHeaderView.Interactive,
                   fixed=QtWidgets.QHeaderView.Fixed,
                   stretch=QtWidgets.QHeaderView.Stretch,
                   resize_to_contents=QtWidgets.QHeaderView.ResizeToContents)

    section_vis_changed = QtCore.Signal(int, bool)

    def __init__(self, orientation=None, parent=None):
        o = QtCore.Qt.Vertical if orientation == "vertical" else QtCore.Qt.Horizontal
        super().__init__(o, parent=parent)
        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self.widget_name = parent.id

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

    def section_labels(self) -> list:
        model = self.parent().model()
        return [model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
                for i in range(self.count())]

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
            fn = functools.partial(self.set_section_hidden, i=i, hide=val)
            act.triggered.connect(fn)
        menu.exec_(self.mapToGlobal(event.pos()))

    def set_section_hidden(self, i: int, hide: bool):
        self.section_vis_changed.emit(i, hide)
        self.setSectionHidden(i, hide)

    def set_sizes(self, sizes: Iterable):
        for i, size in enumerate(sizes):
            if size is not None:
                self.resizeSection(i, size)

    def set_default_section_size(self, size):
        if size is None:
            self.resetDefaultSectionSize()
        else:
            self.setDefaultSectionSize(size)

    def stretch_last_section(self, stretch: bool = True):
        self.setStretchLastSection(stretch)


if __name__ == "__main__":
    app = widgets.app()
    header = HeaderView(parent=None)
    app.exec_()
