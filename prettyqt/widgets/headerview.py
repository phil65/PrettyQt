from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping
import hashlib
import logging
from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


MODES = bidict(
    interactive=QtWidgets.QHeaderView.ResizeMode.Interactive,
    fixed=QtWidgets.QHeaderView.ResizeMode.Fixed,
    stretch=QtWidgets.QHeaderView.ResizeMode.Stretch,
    resize_to_contents=QtWidgets.QHeaderView.ResizeMode.ResizeToContents,
)

ModeStr = Literal["interactive", "fixed", "stretch", "resize_to_contents"]

logger = logging.getLogger(__name__)


class HeaderWrapper:
    def __init__(self, indexer, widget: widgets.QHeaderView):
        self._widget = widget
        self._range = (
            range(
                indexer.start or 0,
                indexer.stop or self._widget.count(),
                indexer.step or 1,
            )
            if isinstance(indexer, slice)
            else range(indexer, indexer + 1)
        )

    def set_hidden(self, hide: bool = True):
        for i in self._range:
            self._widget.setSectionHidden(i, hide)

    def resize(self, size: int | Iterable[int]):
        match size:
            case int():
                for i in self._range:
                    self._widget.resizeSection(i, size)
            case Iterable():
                for i, j in zip(self._range, size):
                    self._widget.resizeSection(i, j)
            case _:
                raise TypeError(size)

    def set_resize_mode(self, mode: ModeStr):
        for i in self._range:
            self._widget.setSectionResizeMode(i, MODES[mode])

    def set_sort_indicator(self, ascending: bool = True):
        sort_order = constants.ASCENDING if ascending else constants.DESCENDING
        for i in self._range:
            self._widget.setSortIndicator(i, sort_order)

    def is_in_visual_range(self) -> bool:
        return self._widget.is_in_visual_range(
            self._range.start
        ) and self._widget.is_in_visual_range(self._range.stop)


class HeaderViewMixin(widgets.AbstractItemViewMixin):
    section_visiblity_changed = core.Signal(int, bool)
    section_resized_by_user = core.Signal(int, int, int)

    def __init__(
        self,
        orientation: constants.OrientationStr | QtCore.Qt.Orientation,
        parent: QtWidgets.QWidget | None = None,
        **kwargs,
    ):
        if isinstance(orientation, QtCore.Qt.Orientation):
            ori = orientation
        else:
            ori = constants.ORIENTATION[orientation]
        super().__init__(ori, parent=parent, **kwargs)
        if ori == constants.HORIZONTAL:
            self.installEventFilter(self)

        self.setSectionsMovable(True)
        self.setSectionsClickable(True)
        self.sectionResized.connect(self._on_section_resize)
        self._handle_section_is_pressed = False
        self.setResizeContentsPrecision(100)
        self._widget_name = parent.objectName() if parent is not None else ""

    def __getitem__(self, index):
        match index:
            case int() if index >= self.count() or index < 0:
                raise IndexError(index)
            case int():
                return HeaderWrapper(index, self)
            case str():
                index = self.get_section_for_label(index)
                return HeaderWrapper(index, self)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"defaultAlignment": constants.ALIGNMENTS}
        return maps

    def set_sort_indicator(self, logical_index: int | None, ascending: bool = True):
        idx = -1 if logical_index is None else logical_index
        sort_order = constants.ASCENDING if ascending else constants.DESCENDING
        self.setSortIndicator(idx, sort_order)

    def set_sections_movable(self, value: bool, include_first: bool = False):
        self.setSectionsMovable(value)
        self.setFirstSectionMovable(include_first)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        shape = self.get_cursor().get_shape()
        self._handle_section_is_pressed = shape == "split_horizontal"

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._handle_section_is_pressed = False

    def _on_section_resize(self, logical_index, old_size, new_size):
        if self._handle_section_is_pressed:
            self.section_resized_by_user.emit(logical_index, old_size, new_size)

    def generate_header_id(self):
        # return f"{self._widget_name}.state"
        column_names = ",".join(self.get_section_labels())
        columns_hash = hashlib.md5(column_names.encode()).hexdigest()
        return f"{type(self).__name__}_{columns_hash}.state"

    def save_state(self, settings: MutableMapping | None = None, key: str | None = None):
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        settings[key] = self.saveState()

    def load_state(self, settings: Mapping | None = None, key: str | None = None) -> bool:
        settings = core.Settings() if settings is None else settings
        key = self.generate_header_id() if key is None else key
        if (state := settings.get(key)) is not None:
            if isinstance(state, str):
                state = state.encode()
            self.restoreState(state)
            return True
        return False

    def resize_sections(self, mode: ModeStr = "resize_to_contents"):
        self.resizeSections(MODES[mode])

    def get_resize_mode(self, col: int) -> ModeStr:
        val = self.sectionResizeMode(col)
        return MODES.inverse[val]

    def set_resize_mode(
        self,
        mode: ModeStr,
        precision: int | None = None,
        cascading: bool | None = None,
        stretch_last_section: bool | None = None,
        default_section_size: int | None = None,
        maximum_section_size: int | None = None,
        minimum_section_size: int | None = None,
    ):
        if stretch_last_section is not None:
            self.stretchLastSection(stretch_last_section)
        if minimum_section_size is not None:
            self.setMinimumSectionSize(minimum_section_size)
        if default_section_size is not None:
            self.setDefaultSectionSize(default_section_size)
        if maximum_section_size is not None:
            self.setMaximumSectionSize(maximum_section_size)
        if precision is not None:
            self.setResizeContentsPrecision(precision)
        if cascading is not None:
            self.setCascadingSectionResizes(cascading)
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.setSectionResizeMode(MODES[mode])

    def get_section_labels(self) -> list[str]:
        """Return all section labels as a list."""
        model = self.model()
        orientation = self.orientation()
        return [
            model.headerData(i, orientation, constants.DISPLAY_ROLE)
            for i in range(self.count())
        ]

    def is_in_visual_range(self, section: int) -> bool:
        if self.orientation() == constants.VERTICAL:
            length = self.height()
            count = self.model().rowCount()
        else:
            length = self.width()
            count = self.model().columnCount()
        if count == 0 or section >= count:
            return False
        start = max(self.visualIndexAt(0), 0)
        end = self.visualIndexAt(length)
        if end == -1:
            end = count - 1
        sections = (self.logicalIndex(i) for i in range(start, end))
        return section in sections

    def get_section_for_label(self, label) -> int:
        """Return index of first section with given label."""
        model = self.model()
        orientation = self.orientation()
        for i in range(self.count()):
            if model.headerData(i, orientation, constants.DISPLAY_ROLE) == label:
                return i
        raise ValueError(label)

    def eventFilter(self, source, event):
        if event.type() == core.Event.Type.ContextMenu:
            menu = self.createPopupMenu()
            menu.exec(self.mapToGlobal(event.pos()))
            logger.info(f"KeypressEvent {event} taken by EventFilter")
            return True
        return False

    def get_header_actions(self) -> list[gui.Action]:
        menu = self.createPopupMenu()
        return menu.actions()

    def createPopupMenu(self) -> widgets.Menu:
        menu = widgets.Menu(parent=self)
        actions = []
        labels = self.get_section_labels()[1:]
        for i, header_label in enumerate(labels, start=1):
            val = not self.isSectionHidden(i)
            action = gui.Action(
                text=str(header_label),
                checkable=True,
                checked=val,
                triggered=self._on_toggle_action_triggered,
            )
            action.setData(i)
            actions.append(action)
        menu.add_actions(actions)
        return menu

    def _on_toggle_action_triggered(self):
        action = self.sender()
        section = action.data()
        self.toggle_section_visibility(section)

    def toggle_section_visibility(self, logical_index: int):
        self.setSectionHidden(logical_index, not self.isSectionHidden(logical_index))
        logger.info(f"toggling {logical_index}")

    def setSectionHidden(self, logical_index: int, hide: bool):
        self.section_visiblity_changed.emit(logical_index, hide)
        super().setSectionHidden(logical_index, hide)

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

    def get_default_alignment(self) -> constants.AlignmentStr:
        return constants.ALIGNMENTS.inverse[self.defaultAlignment()]

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]


class HeaderView(HeaderViewMixin, QtWidgets.QHeaderView):
    pass


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    table = debugging.example_tree()
    table.h_header[1:].set_hidden(True)
    table.show()

    with app.debug_mode():
        app.main_loop()
