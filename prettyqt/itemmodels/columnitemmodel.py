import enum
import logging
from typing import TYPE_CHECKING, Any

from prettyqt import constants, core, itemmodels


if TYPE_CHECKING:
    from collections.abc import Sequence

    from prettyqt import gui


logger = logging.getLogger(__name__)

SMALL_COL_WIDTH = 120
MEDIUM_COL_WIDTH = 200


class ColumnItem:
    """Determines how an object attribute is shown."""

    model: core.QAbstractItemModel
    name: str = ""
    doc: str = "<no help available>"
    col_visible: bool = True
    width: int | str = SMALL_COL_WIDTH
    line_wrap: gui.textoption.WordWrapModeStr = "none"
    selectable: bool = True
    enabled: bool = True
    editable: bool = False
    checkable: bool = False
    tristate: bool = False

    def __init__(self, model: core.QAbstractItemModel):
        self.model = model

    def get_name(self) -> str:
        return self.name

    def get_flags(self, tree_item):
        flag = constants.NO_FLAGS
        if self.selectable:
            flag |= constants.IS_SELECTABLE
        if self.enabled:
            flag |= constants.IS_ENABLED
        if self.editable:
            flag |= constants.IS_EDITABLE
        if self.checkable:
            flag |= constants.IS_CHECKABLE
        if self.tristate:
            flag |= constants.IS_USER_TRISTATE
        return flag

    def get_data(self, item, role):
        return NotImplemented

    def set_data(self, item, value, role):
        return NotImplemented

    def get_width(self) -> int:
        match self.width:
            case "small":
                return SMALL_COL_WIDTH
            case "medium":
                return MEDIUM_COL_WIDTH
            case int():
                return self.width
            case _:
                raise ValueError(self.width)

    @staticmethod
    def to_checkstate(value: bool):
        return constants.CheckState.Checked if value else constants.CheckState.Unchecked


class ColumnItemModelMixin:
    class ExtraRoles(enum.IntEnum):
        """Addional roles."""

        TreeItemRole = constants.USER_ROLE + 43435
        ColumnItemRole = constants.USER_ROLE + 43436

    _attr_cols: list[ColumnItem]

    def set_columns(self, columns: Sequence[type[ColumnItem]]):
        self._attr_cols = [Col(model=self) for Col in columns]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        """Return the tree item at the given index and role."""
        if not index.isValid():
            return None
        tree_item = self.data_by_index(index)
        col_item = self._attr_cols[index.column()]
        match role:
            case self.ExtraRoles.TreeItemRole:
                return tree_item
            case self.ExtraRoles.ColumnItemRole:
                return col_item
            case _:
                result = col_item.get_data(tree_item, role)
                return None if result is NotImplemented else result

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        tree_item = self.data_by_index(index)
        col_item = self._attr_cols[index.column()]
        # set_data implementations may return None for success (legacy behaviour)
        result = col_item.set_data(tree_item, value, role)
        if result is NotImplemented or result is False:
            return False
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        if not index.isValid():
            return super().flags(index)
        tree_item = self.data_by_index(index)
        return self._attr_cols[index.column()].get_flags(tree_item)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if (
                0 <= section < len(self._attr_cols)
            ):
                return self._attr_cols[section].get_name()
            case constants.HORIZONTAL, constants.TOOLTIP_ROLE if (
                0 <= section < len(self._attr_cols)
            ):
                return self._attr_cols[section].doc
        return None


class ColumnItemModel(ColumnItemModelMixin, itemmodels.TreeModel):
    """TreeModel with columns defined by ColumnItem classes."""

    def __init__(
        self,
        obj=None,
        columns: Sequence[type[ColumnItem]] = (),
        mime_type: str | None = None,
        show_root: bool = True,
        **kwargs,
    ):
        # columns need to be available before the TreeModel fetches the root.
        self.mime_type = mime_type
        self.set_columns(columns)
        super().__init__(obj=obj, show_root=show_root, **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        return len(self._attr_cols)


class ColumnTableModel(
    itemmodels.ListMixin, ColumnItemModelMixin, core.AbstractTableModel
):
    """List-based table model with columns defined by ColumnItem classes."""

    def __init__(
        self,
        items: Sequence | None = None,
        columns: Sequence[type[ColumnItem]] = (),
        mime_type: str | None = None,
        **kwargs,
    ):
        self.set_columns(columns)
        self.mime_type = mime_type
        self.MIME_TYPE = mime_type or ""
        super().__init__(items=items, **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._attr_cols)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    test = {}

    class TestColumn(ColumnItem):
        name = "test"
        checkable = True

        def get_data(self, item, role):
            match role:
                case constants.CHECKSTATE_ROLE:
                    return getattr(item, "test", False)
                case constants.DISPLAY_ROLE:
                    return str(item.get_root_path())
                case constants.USER_ROLE:
                    return str(item.get_root_path())

        def set_data(self, item, value, role):
            match role:
                case constants.CHECKSTATE_ROLE:
                    item.test = value

    items = core.StorageInfo.get_mounted_volumes()
    model = ColumnTableModel(items, [TestColumn])
    table = widgets.TableView()
    table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.exec()
