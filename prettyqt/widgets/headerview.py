# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Optional, Callable, Iterable

from qtpy import QtCore, QtWidgets


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

    def contextMenuEvent(self, event):
        """
        context menu for our files tree
        """
        menu = QtWidgets.QMenu(parent=self)
        for i, header_label in enumerate(self.section_labels()[1:], start=1):
            act = menu.addAction(header_label)
            act.setCheckable(True)
            val = not self.isSectionHidden(i)
            act.setChecked(val)
            self.setSectionHidden(i, val)
            self.section_vis_changed.emit(i, val)
        menu.exec_(self.mapToGlobal(event.pos()))

    def set_custom_menu(self, method: Callable):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(method)

    def set_sizes(self, sizes: Iterable):
        for i, size in enumerate(sizes):
            if size is not None:
                self.resizeSection(i, size)
