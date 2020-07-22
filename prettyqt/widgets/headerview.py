# -*- coding: utf-8 -*-
"""
"""

import functools
from typing import Iterable, Optional, Union, List

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, helpers


ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)

MODES = bidict(
    interactive=QtWidgets.QHeaderView.Interactive,
    fixed=QtWidgets.QHeaderView.Fixed,
    stretch=QtWidgets.QHeaderView.Stretch,
    resize_to_contents=QtWidgets.QHeaderView.ResizeToContents,
)


QtWidgets.QHeaderView.__bases__ = (widgets.AbstractItemView,)


class HeaderView(QtWidgets.QHeaderView):

    section_vis_changed = QtCore.Signal(int, bool)

    def __init__(
        self, orientation: Union[str, int], parent: Optional[QtWidgets.QWidget] = None
    ):
        if orientation in ORIENTATIONS:
            orientation = ORIENTATIONS[orientation]
        super().__init__(orientation, parent=parent)
        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self._widget_name = parent.id if parent is not None else ""

    def save_state(self):
        settings = core.Settings()
        settings.setValue(f"{self._widget_name}.state", self.saveState())

    def load_state(self):
        settings = core.Settings()
        state = settings.get(f"{self._widget_name}.state", None)
        if state is not None:
            self.restoreState(state)

    def resize_sections(self, mode: str):
        self.resizeSections(MODES[mode])

    @helpers.deprecated
    def resize_mode(self, mode: str, col: Optional[int] = None):
        self.set_resize_mode(mode, col)

    def set_resize_mode(self, mode: str, col: Optional[int] = None):
        if mode not in MODES:
            raise ValueError("mode not existing")
        if col is None:
            self.setSectionResizeMode(MODES[mode])
        else:
            self.setSectionResizeMode(col, MODES[mode])

    def section_labels(self) -> List[str]:
        model = self.parent().model()
        return [
            model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
            for i in range(self.count())
        ]

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

    def set_default_section_size(self, size: Optional[int]):
        if size is None:
            self.resetDefaultSectionSize()
        else:
            self.setDefaultSectionSize(size)

    def stretch_last_section(self, stretch: bool = True):
        self.setStretchLastSection(stretch)


if __name__ == "__main__":
    app = widgets.app()
    header = HeaderView("horizontal")
    header.show()
    app.exec_()
