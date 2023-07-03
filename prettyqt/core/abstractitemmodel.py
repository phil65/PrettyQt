from __future__ import annotations

from collections.abc import Iterator, Sequence
import contextlib
import logging

from typing import Any, Literal, overload

from prettyqt import constants, core
from prettyqt.utils import bidict, helpers, listdelegators


logger = logging.getLogger(__name__)

CheckIndexOptionStr = Literal[
    "none", "index_is_valid", "do_not_use_parent", "parent_is_invalid"
]

CHECK_INDEX_OPTIONS: bidict[
    CheckIndexOptionStr, core.QAbstractItemModel.CheckIndexOption
] = bidict(
    none=core.QAbstractItemModel.CheckIndexOption.NoOption,
    index_is_valid=core.QAbstractItemModel.CheckIndexOption.IndexIsValid,
    do_not_use_parent=core.QAbstractItemModel.CheckIndexOption.DoNotUseParent,
    parent_is_invalid=core.QAbstractItemModel.CheckIndexOption.ParentIsInvalid,
)

LayoutChangeHintStr = Literal["none", "vertical_sort", "horizontal_sort"]

LAYOUT_CHANGE_HINT: bidict[
    LayoutChangeHintStr, core.QAbstractItemModel.LayoutChangeHint
] = bidict(
    none=core.QAbstractItemModel.LayoutChangeHint.NoLayoutChangeHint,
    vertical_sort=core.QAbstractItemModel.LayoutChangeHint.VerticalSortHint,
    horizontal_sort=core.QAbstractItemModel.LayoutChangeHint.HorizontalSortHint,
)


class AbstractItemModelMixin(core.ObjectMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED | constants.IS_ENABLED | constants.IS_SELECTABLE
    )

    def __repr__(self):
        return f"{type(self).__name__}: ({self.rowCount()}, {self.columnCount()})"

    def __len__(self) -> int:
        return self.rowCount()

    def __add__(self, other: core.QAbstractItemModel) -> core.ConcatenateTablesProxyModel:
        proxy = core.ConcatenateTablesProxyModel()
        proxy.addSourceModel(self)
        proxy.addSourceModel(other)
        return proxy

    @overload
    def __getitem__(self, index: tuple[int, int] | int) -> core.ModelIndex:
        ...

    @overload
    def __getitem__(
        self, index: tuple[slice, int] | tuple[int, slice] | tuple[slice, slice]
    ) -> listdelegators.BaseListDelegator[core.ModelIndex]:
        ...

    def __getitem__(
        self, index: tuple[int | slice, int | slice]
    ) -> core.ModelIndex | listdelegators.BaseListDelegator[core.ModelIndex]:
        # TODO: do proxies need mapToSource here?
        rowcount = self.rowCount()
        colcount = self.columnCount()
        match index:
            case int() as row, int() as col:
                if row >= rowcount or col >= rowcount:
                    raise IndexError(index)
                return self.index(row, col)
            case (row, col):
                indexes = [
                    self.index(i, j)
                    for i, j in helpers.yield_positions(row, col, rowcount, colcount)
                ]
                return listdelegators.BaseListDelegator(indexes)
            case int() as row:
                if row >= rowcount:
                    raise IndexError(index)
                # this here breaks PySide6 IPython test...
                return self.index(row, 0)
            case _:
                raise TypeError(index)

    def set_data(
        self,
        index: tuple[int | slice, int | slice] | core.ModelIndex,
        value: Any,
        role=constants.EDIT_ROLE,
    ):
        match index:
            case core.ModelIndex():
                self.setData(index, value, role)
            case (row, col):
                rowcount = self.rowCount()
                colcount = self.columnCount()
                for i, j in helpers.yield_positions(row, col, rowcount, colcount):
                    self.setData(self.index(i, j), value, role)
            case _:
                raise TypeError(index)

    def check_index(
        self,
        index: core.ModelIndex,
        index_is_valid: bool = False,
        do_not_use_parent: bool = False,
        parent_is_invalid: bool = False,
    ) -> bool:
        flag = core.QAbstractItemModel.CheckIndexOption.NoOption
        if index_is_valid:
            flag |= core.QAbstractItemModel.CheckIndexOption.IndexIsValid
        if do_not_use_parent:
            flag |= core.QAbstractItemModel.CheckIndexOption.DoNotUseParent
        if parent_is_invalid:
            flag |= core.QAbstractItemModel.CheckIndexOption.ParentIsInvalid
        check_flag = core.QAbstractItemModel.CheckIndexOption(0) | flag
        return self.checkIndex(index, check_flag)

    @contextlib.contextmanager
    def change_layout(self):
        """Context manager to change the layout.

        wraps calls with correct signals
        emitted at beginning: layoutAboutToBeChanged
        emitted at end: layoutChanged

        """
        self.layoutAboutToBeChanged.emit()
        yield None
        self.layoutChanged.emit()

    @contextlib.contextmanager
    def reset_model(self):
        """Context manager to reset the model.

        wraps calls with correct signals
        emitted at beginning: beginResetModel
        emitted at end: endResetModel

        """
        self.beginResetModel()
        yield None
        self.endResetModel()

    def get_column_type(
        self,
        column: int,
        rows_to_check: int = 10,
        role=constants.DISPLAY_ROLE,
    ) -> type | None:
        """Guess column data type by checking values of first rows with given role."""
        to_check = min(rows_to_check, self.rowCount())
        if to_check == 0:
            return None
        # cant combine these or make them a generator, so we do two list comps.
        indexes = [self.index(row, column) for row in range(to_check)]
        values = [self.data(i, role=role) for i in indexes]
        if all(isinstance(i, bool) for i in values):
            return bool
        if all(isinstance(i, str) for i in values):
            return str
        if all(isinstance(i, int) for i in values):
            return int
        if all(isinstance(i, float) for i in values):
            return float
        check_values = [self.data(i, role=constants.CHECKSTATE_ROLE) for i in indexes]
        return bool if None not in check_values else None

    def update_row(self, row: int):
        start_index = self.index(row, 0)
        end_index = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(start_index, end_index)

    def update_all(self):
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)

    @contextlib.contextmanager
    def remove_row(self, row: int, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        self.beginRemoveRows(parent, row, row)
        yield None
        self.endRemoveRows()

    @contextlib.contextmanager
    def remove_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: core.ModelIndex | None = None,
    ):
        parent = core.ModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveRows(parent, first, last)
        yield None
        self.endRemoveRows()

    @contextlib.contextmanager
    def remove_columns(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: core.ModelIndex | None = None,
    ):
        parent = core.ModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveColumns(parent, first, last)
        yield None
        self.endRemoveColumns()

    @contextlib.contextmanager
    def insert_row(self, row: int, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        self.beginInsertRows(parent, row, row)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: core.ModelIndex | None = None,
    ):
        parent = core.ModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def append_rows(self, num_rows: int, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        row_count = self.rowCount()
        self.beginInsertRows(parent, row_count, row_count + num_rows - 1)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_columns(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: core.ModelIndex | None = None,
    ):
        parent = core.ModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginInsertColumns(parent, first, last)
        yield None
        self.endInsertColumns()

    def force_reset(self):
        self.beginResetModel()
        self.endResetModel()

    def force_layoutchange(self):
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def get_role_names(self) -> bidict[int, str]:
        return bidict({i: v.data().decode() for i, v in self.roleNames().items()})

    def get_breadcrumbs_path(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> list[str]:
        """Get the path for the given index.

        Returns a list containing data of all indexes up to the root for given role.
        """
        pieces = [index.data(role)]
        while (index := index.parent()).isValid():
            pieces.insert(0, index.data(role))
        return pieces

    def iter_tree(
        self,
        parent_index: core.ModelIndex | None = None,
        depth: int | None = None,
        fetch_more: bool = False,
    ) -> Iterator[core.ModelIndex]:
        """Iter through all indexes of the model tree.

        Arguments:
            parent_index: parent index
            depth: maximum iteration depth
            fetch_more: call fetchMore for all indexes until canFetchMore returns False
        """
        if parent_index is None:
            # TODO: does this always equal AbstractItemView.rootIndex()?
            # parent_index = self.index(0, 0)
            parent_index = core.ModelIndex()
        if parent_index.isValid():
            yield parent_index
            if fetch_more:
                while self.canFetchMore(parent_index):
                    self.fetchMore(parent_index)
        if depth is not None and (depth := depth - 1) < 0:
            return
        for i in range(self.rowCount(parent_index)):
            child_index = self.index(i, 0, parent_index)
            yield from self.iter_tree(child_index, depth, fetch_more=fetch_more)

    def search_tree(
        self,
        value: Any,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
        parent_index: core.ModelIndex | None = None,
        max_results: int | None = None,
        depth: int | None = None,
    ) -> listdelegators.BaseListDelegator[core.ModelIndex]:
        """Search the tree for indexes with a given value in given role.

        Compared to QAbstractItemModel.match, this method allows to set a maximum
        search depth and passing several values to search for as a list.

        Arguments:
            value: Item or list of items to search for.
            role: Index role to search in.
            parent_index: start index for searching. If None, whole tree is searched.
            max_results: stop searching after x amount of hits. 'None' means no limit.
            depth: search depth. Search depth. 'None' means no limit.
        """
        results = []
        # This makes it impossible to search for lists. I think thats fine.
        if not isinstance(value, list):
            value = [value]
        for idx in self.iter_tree(parent_index, depth=depth):
            if self.data(idx, role) in value:
                results.append(idx)
                if len(results) == max_results:
                    break
        return listdelegators.BaseListDelegator(results)

    def get_child_indexes(
        self, index: core.ModelIndex
    ) -> listdelegators.BaseListDelegator[core.ModelIndex]:
        """Get all child indexes for given index (first column only).

        To get indexes recursively, use iter_tree.

        Arguments:
            index: ModelIndex to get children from
        """
        indexes = [self.index(i, 0, index) for i in range(self.rowCount(index))]
        return listdelegators.BaseListDelegator(indexes)

    def get_index_key(
        self,
        index: core.ModelIndex,
        include_column: bool = False,
        parent_index: core.ModelIndex | None = None,
    ) -> tuple[tuple[int, int], ...]:
        """Return a key tuple for given ModelIndex.

        The key tuple consists either of row integers or (row, column) indices
        describing the index position from top to bottom.

        Arguments:
            index: ModelIndex to get a key for
            include_column: whether to include the column in the index key.
            parent_index: Get key up to given ModelIndex. By default, get key up to root.
        """
        key_path = []
        parent = index
        while parent.isValid() and parent != parent_index:
            key = (parent.row(), parent.column()) if include_column else parent.row()
            key_path.append(key)
            parent = parent.parent()
        return tuple(reversed(key_path))

    def index_from_key(
        self,
        key_path: Sequence[tuple[int, int] | int],
        parent_index: core.ModelIndex | None = None,
    ) -> core.ModelIndex:
        """Return a source QModelIndex for the given key.

        Arguments:
            key_path: Key path to get an index for.
                      Should be a sequence of either (row, column)  or row indices
            parent_index: ModelIndex to start indexing from. Defaults to root index.
        """
        model = self.sourceModel()
        if model is None:
            return core.ModelIndex()
        index = parent_index or core.ModelIndex()
        for key in key_path:
            key = (key, 0) if isinstance(key, int) else key
            index = model.index(*key, index)
        return index

    @staticmethod
    def to_checkstate(value: bool):
        return constants.CheckState.Checked if value else constants.CheckState.Unchecked


class AbstractItemModel(AbstractItemModelMixin, core.QAbstractItemModel):
    pass

    # @abc.abstractmethod
    # def index(self, *args, **kwargs):
    #     return NotImplemented

    # # this one is only abstract for a specific signature.
    # # @abc.abstractmethod
    # # def parent(self, *args, **kwargs):
    # #     return NotImplemented

    # @abc.abstractmethod
    # def rowCount(self, *args, **kwargs):
    #     return NotImplemented

    # @abc.abstractmethod
    # def columnCount(self, *args, **kwargs):
    #     return NotImplemented

    # @abc.abstractmethod
    # def data(self, *args, **kwargs):
    #     return NotImp


if __name__ == "__main__":

    class Test(AbstractItemModel):
        pass
