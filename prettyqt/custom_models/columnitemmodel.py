from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Callable

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


@dataclass(frozen=True)
class ColumnItem:
    """Determines how an object attribute is shown."""

    name: str
    label: Callable | None
    checkstate: Callable | None = None
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

    def get_label(self, tree_item):
        if self.label is None:
            return ""
        elif callable(self.label):
            return self.label(tree_item)
        return self.label

    def get_checkstate(self, tree_item):
        if self.checkstate is None:
            return None
        elif callable(self.checkstate):
            return self.checkstate(tree_item)
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


class ColumnItemModel(core.AbstractItemModel):
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

    def data(self, index, role):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None

        col = index.column()
        tree_item = index.internalPointer()

        if role in [constants.DISPLAY_ROLE, constants.EDIT_ROLE]:
            val = self._attr_cols[col].get_label(tree_item)
            return val.replace("\n", " ")
        elif role == constants.DECORATION_ROLE:
            return self._attr_cols[col].get_decoration(tree_item)
        elif role == constants.CHECKSTATE_ROLE:
            return self._attr_cols[col].get_checkstate(tree_item)
        elif role == constants.ALIGNMENT_ROLE:
            return self._attr_cols[col].get_alignment(tree_item)
        elif role == constants.FOREGROUND_ROLE:
            return self._attr_cols[col].get_foreground_color(tree_item)
        elif role == constants.BACKGROUND_ROLE:
            return self._attr_cols[col].get_background_color(tree_item)
        elif role == constants.FONT_ROLE:
            return self._attr_cols[col].get_font(tree_item)
        else:
            return None

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
