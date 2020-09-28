# -*- coding: utf-8 -*-

import functools
from typing import Iterable, Optional, Union, List

from deprecated import deprecated
from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


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

    def save_state(
        self, settings: Optional[core.Settings] = None, key: Optional[str] = None
    ):
        settings = core.Settings() if settings is None else settings
        key = f"{self._widget_name}.state" if key is None else key
        settings.set_value(key, self.saveState())

    def load_state(
        self, settings: Optional[core.Settings] = None, key: Optional[str] = None
    ) -> bool:
        settings = core.Settings() if settings is None else settings
        key = f"{self._widget_name}.state" if key is None else key
        state = settings.get(key, None)
        if state is not None:
            self.restoreState(state)
            return True
        return False

    def resize_sections(self, mode: str):
        self.resizeSections(MODES[mode])

    @deprecated(reason="This method is deprecated, use set_resize_mode instead.")
    def resize_mode(self, mode: str, col: Optional[int] = None):
        self.set_resize_mode(mode, col)

    def set_resize_mode(self, mode: str, col: Optional[int] = None):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        if col is None:
            self.setSectionResizeMode(MODES[mode])
        else:
            self.setSectionResizeMode(col, MODES[mode])

    def get_section_labels(self) -> List[str]:
        model = self.model()
        return [
            model.headerData(i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
            for i in range(self.count())
        ]

    def contextMenuEvent(self, event):
        """Context menu for our files tree."""
        menu = widgets.Menu(parent=self)
        actions = self.get_header_actions()
        menu.add_actions(actions)
        menu.exec_(self.mapToGlobal(event.pos()))

    def get_header_actions(self) -> List[widgets.Action]:
        actions = list()
        labels = self.get_section_labels()[1:]
        for i, header_label in enumerate(labels, start=1):
            val = not self.isSectionHidden(i)
            action = widgets.Action(text=header_label, checkable=True, checked=val)
            fn = functools.partial(self.set_section_hidden, i=i, hide=val)
            action.triggered.connect(fn)
            actions.append(action)
        return actions

    def set_section_hidden(self, i: int, hide: bool):
        self.section_vis_changed.emit(i, hide)
        self.setSectionHidden(i, hide)

    def set_sizes(self, sizes: Iterable[Optional[int]]):
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
    app.main_loop()
