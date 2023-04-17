from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import treeitem


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


@dataclass(frozen=True)
class ColumnItem:
    """Determines how an object attribute is shown."""

    name: str
    label: Callable[[treeitem.TreeItem], str] | None
    checkstate: Callable[
        [treeitem.TreeItem], constants.StateStr | QtCore.Qt.CheckState | bool
    ] | None = None
    sort_value: Callable[[treeitem.TreeItem], str | float] | None = None
    tooltip: Callable[[treeitem.TreeItem], str] | None = None
    doc: str = "<no help available>"
    col_visible: bool = True
    width: int | str = SMALL_COL_WIDTH
    alignment: Callable | int | None = None
    line_wrap: gui.textoption.WordWrapModeStr = "none"
    foreground_color: Callable | str | None = None
    background_color: Callable | str | None = None
    decoration: Callable | QtGui.QIcon | None = None
    font: Callable | QtGui.QFont | None = None
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False
    user_data: dict | Callable | None = None

    def get_name(self) -> str:
        return self.name

    def get_flag(self):
        flag = constants.NO_FLAGS
        if self.selectable:
            flag |= constants.IS_SELECTABLE  # type: ignore
        if self.enabled:
            flag |= constants.IS_ENABLED  # type: ignore
        if self.editable:
            flag |= constants.IS_EDITABLE  # type: ignore
        if self.checkable:
            flag |= constants.IS_CHECKABLE  # type: ignore
        if self.tristate:
            flag |= constants.IS_USER_TRISTATE  # type: ignore
        return flag

    def get_label(self, tree_item) -> str:
        if self.label is None:
            return ""
        elif callable(self.label):
            return self.label(tree_item)
        return self.label

    def get_sort_value(self, tree_item) -> str | int:
        if self.sort_value is None:
            return self.get_label()
        elif callable(self.sort_value):
            return self.sort_value(tree_item)
        return self.sort_value

    def get_user_data(self, tree_item, role):
        if self.user_data is None:
            return ""
        elif callable(self.user_data):
            return self.user_data(tree_item, role)
        return self.user_data[role]

    def get_tooltip(self, tree_item) -> str:
        if self.tooltip is None:
            return ""
        elif callable(self.tooltip):
            return self.tooltip(tree_item)
        return self.tooltip

    def get_checkstate(self, tree_item):
        if self.checkstate is None:
            return None
        elif callable(self.checkstate):
            result = self.checkstate(tree_item)
            if isinstance(result, str):
                result = constants.STATE[result]
            return result
        return self.checkstate

    def get_font(self, tree_item):
        if self.font is None:
            return None
        elif callable(self.font):
            return self.font(tree_item)
        return self.font

    def get_foreground_color(self, tree_item):
        if self.foreground_color is None:
            return None
        elif callable(self.foreground_color):
            return self.foreground_color(tree_item)
        return self.foreground_color

    def get_background_color(self, tree_item):
        if self.background_color is None:
            return None
        elif callable(self.background_color):
            return self.background_color(tree_item)
        return self.background_color

    def get_decoration(self, tree_item):
        if self.decoration is None:
            return None
        elif callable(self.decoration):
            return self.decoration(tree_item)
        return self.decoration

    def get_alignment(self, tree_item) -> int:
        if self.alignment is None:
            return constants.ALIGN_LEFT  # type: ignore
        elif callable(self.alignment):
            return self.alignment(tree_item)
        elif isinstance(self.alignment, str):
            return constants.ALIGNMENTS[self.alignment]
        return self.alignment

    def get_width(self) -> int:
        if self.width == "small":
            return SMALL_COL_WIDTH
        elif self.width == "medium":
            return MEDIUM_COL_WIDTH
        elif isinstance(self.width, int):
            return self.width
        raise ValueError(self.width)


class ColumnItemModelMixin:
    """Model that provides an interface to an objectree that is build of TreeItems."""

    def __init__(
        self,
        attr_cols: list[ColumnItem] | None = None,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(parent)
        self._attr_cols = attr_cols if attr_cols is not None else []

    def columnCount(self, _parent=None):
        """Return the number of columns in the tree."""
        return len(self._attr_cols)

    def tree_item(self, index: core.ModelIndex) -> treeitem.TreeItem:
        if not index.isValid():
            return None
        else:
            return index.internalPointer()  # type: ignore

    def data(self, index, role):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = self.tree_item(index)

        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                val = self._attr_cols[col].get_label(tree_item)
                return val.replace("\n", " ")
            case constants.DECORATION_ROLE:
                return self._attr_cols[col].get_decoration(tree_item)
            case constants.CHECKSTATE_ROLE:
                return self._attr_cols[col].get_checkstate(tree_item)
            case constants.ALIGNMENT_ROLE:
                return self._attr_cols[col].get_alignment(tree_item)
            case constants.FOREGROUND_ROLE:
                return self._attr_cols[col].get_foreground_color(tree_item)
            case constants.BACKGROUND_ROLE:
                return self._attr_cols[col].get_background_color(tree_item)
            case constants.FONT_ROLE:
                return self._attr_cols[col].get_font(tree_item)
            case constants.SORT_ROLE:
                return self._attr_cols[col].get_sort_value(tree_item)
            case constants.TOOLTIP_ROLE:
                return self._attr_cols[col].get_tooltip(tree_item)
            case _:
                return self._attr_cols[col].user_data.get(role)

    def flags(self, index):
        if not index.isValid():
            return constants.NO_CHILDREN
        col = index.column()
        return self._attr_cols[col].get_flag()

    def headerData(self, section, orientation, role):
        if orientation == constants.HORIZONTAL and role == constants.DISPLAY_ROLE:
            return self._attr_cols[section].name
        else:
            return None


class ColumnItemModel(ColumnItemModelMixin, core.AbstractItemModel):
    pass


class ColumnTableModel(ColumnItemModelMixin, core.AbstractTableModel):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    class TestModel(ColumnItemModel):
        def rowCount(self, parent=None):
            return 5

    app = widgets.app()
    item = ColumnItem(name="Test", label=None)
    model = TestModel(attr_cols=[item])
    table = widgets.TableView()
    table.set_model(model)
    table.show()
    app.main_loop()
