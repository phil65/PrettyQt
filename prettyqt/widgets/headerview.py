from __future__ import annotations

from collections.abc import Iterable
import functools
import hashlib
from typing import Literal

from deprecated import deprecated

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    interactive=QtWidgets.QHeaderView.ResizeMode.Interactive,
    fixed=QtWidgets.QHeaderView.ResizeMode.Fixed,
    stretch=QtWidgets.QHeaderView.ResizeMode.Stretch,
    resize_to_contents=QtWidgets.QHeaderView.ResizeMode.ResizeToContents,
)

ModeStr = Literal["interactive", "fixed", "stretch", "resize_to_contents"]

QtWidgets.QHeaderView.__bases__ = (widgets.AbstractItemView,)


class HeaderView(QtWidgets.QHeaderView):

    section_vis_changed = core.Signal(int, bool)
    section_resized_by_user = core.Signal(int, int, int)

    def __init__(
        self,
        orientation: constants.OrientationStr | QtCore.Qt.Orientation,
        parent: QtWidgets.QWidget | None = None,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent=parent)
        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self.sectionResized.connect(self.sectionResizeEvent)
        self._handle_section_is_pressed = False
        self._widget_name = parent.get_id() if parent is not None else ""

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self._handle_section_is_pressed = self.cursor().shape() == QtCore.Qt.SplitHCursor

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._handle_section_is_pressed = False

    def sectionResizeEvent(self, logical_index, old_size, new_size):
        if self._handle_section_is_pressed:
            self.section_resized_by_user.emit(logical_index, old_size, new_size)

    def generate_header_id(self):
        # return f"{self._widget_name}.state"
        column_names = ",".join(self.get_section_labels())
        columns_hash = hashlib.md5(column_names.encode()).hexdigest()
        return f"{type(self).__name__}_{columns_hash}.state"

    def save_state(self, settings: core.Settings | None = None, key: str | None = None):
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        settings.set_value(key, self.saveState())

    def load_state(
        self, settings: core.Settings | None = None, key: str | None = None
    ) -> bool:
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        state = settings.get(key, None)
        if state is not None:
            if isinstance(state, str):
                state = state.encode()
            self.restoreState(state)
            return True
        return False

    def resize_sections(self, mode: ModeStr):
        self.resizeSections(MODES[mode])

    @deprecated(reason="This method is deprecated, use set_resize_mode instead.")
    def resize_mode(self, mode: ModeStr, col: int | None = None):
        self.set_resize_mode(mode, col)

    def set_resize_mode(self, mode: ModeStr, col: int | None = None):
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        if col is None:
            self.setSectionResizeMode(MODES[mode])
        else:
            self.setSectionResizeMode(col, MODES[mode])

    def get_section_labels(self) -> list[str]:
        model = self.model()
        return [
            model.headerData(
                i, constants.HORIZONTAL, constants.DISPLAY_ROLE  # type: ignore
            )
            for i in range(self.count())
        ]

    def contextMenuEvent(self, event):
        """Context menu for our files tree."""
        menu = widgets.Menu(parent=self)
        actions = self.get_header_actions()
        menu.add_actions(actions)
        menu.exec_(self.mapToGlobal(event.position()))

    def get_header_actions(self) -> list[widgets.Action]:
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

    def set_sizes(self, sizes: Iterable[int | None]):
        for i, size in enumerate(sizes):
            if size is not None:
                self.resizeSection(i, size)

    def set_default_section_size(self, size: int | None):
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
