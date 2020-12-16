import functools
import hashlib
from typing import Iterable, List, Literal, Optional, Union

from deprecated import deprecated
from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, widgets
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    interactive=QtWidgets.QHeaderView.Interactive,
    fixed=QtWidgets.QHeaderView.Fixed,
    stretch=QtWidgets.QHeaderView.Stretch,
    resize_to_contents=QtWidgets.QHeaderView.ResizeToContents,
)

ModeStr = Literal["interactive", "fixed", "stretch", "resize_to_contents"]

QtWidgets.QHeaderView.__bases__ = (widgets.AbstractItemView,)


class HeaderView(QtWidgets.QHeaderView):

    section_vis_changed = QtCore.Signal(int, bool)

    def __init__(
        self,
        orientation: Union[constants.OrientationStr, int],
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in constants.ORIENTATION:
            orientation = constants.ORIENTATION[orientation]
        super().__init__(orientation, parent=parent)
        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self._widget_name = parent.get_id() if parent is not None else ""

    def generate_header_id(self):
        # return f"{self._widget_name}.state"
        column_names = ",".join(self.get_section_labels())
        columns_hash = hashlib.md5(column_names.encode("utf-8")).hexdigest()
        return f"{type(self).__name__}_{columns_hash}.state"

    def save_state(
        self, settings: Optional[core.Settings] = None, key: Optional[str] = None
    ):
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        settings.set_value(key, self.saveState())

    def load_state(
        self, settings: Optional[core.Settings] = None, key: Optional[str] = None
    ) -> bool:
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        state = settings.get(key, None)
        if state is not None:
            self.restoreState(state)
            return True
        return False

    def resize_sections(self, mode: ModeStr):
        self.resizeSections(MODES[mode])

    @deprecated(reason="This method is deprecated, use set_resize_mode instead.")
    def resize_mode(self, mode: ModeStr, col: Optional[int] = None):
        self.set_resize_mode(mode, col)

    def set_resize_mode(self, mode: ModeStr, col: Optional[int] = None):
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
