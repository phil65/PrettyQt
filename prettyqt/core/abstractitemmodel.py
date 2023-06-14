from __future__ import annotations

import contextlib
import logging
from typing import Any

from collections.abc import Iterator

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, listdelegators


logger = logging.getLogger(__name__)

CHECK_INDEX_OPTIONS = bidict(
    none=QtCore.QAbstractItemModel.CheckIndexOption.NoOption,
    index_is_valid=QtCore.QAbstractItemModel.CheckIndexOption.IndexIsValid,
    do_not_use_parent=QtCore.QAbstractItemModel.CheckIndexOption.DoNotUseParent,
    parent_is_invalid=QtCore.QAbstractItemModel.CheckIndexOption.ParentIsInvalid,
)

LAYOUT_CHANGE_HINT = bidict(
    none=QtCore.QAbstractItemModel.LayoutChangeHint.NoLayoutChangeHint,
    vertical_sort=QtCore.QAbstractItemModel.LayoutChangeHint.VerticalSortHint,
    horizontal_sort=QtCore.QAbstractItemModel.LayoutChangeHint.HorizontalSortHint,
)


class AbstractItemModelMixin(core.ObjectMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED | constants.IS_ENABLED | constants.IS_SELECTABLE
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from prettyqt.utils import proxifier

        self.proxifier = proxifier.Proxyfier(self)

    def __repr__(self):
        return f"{type(self).__name__}: ({self.rowCount()}, {self.columnCount()})"

    def __len__(self) -> int:
        return self.rowCount()

    def __add__(
        self, other: QtCore.QAbstractItemModel
    ) -> core.ConcatenateTablesProxyModel:
        proxy = core.ConcatenateTablesProxyModel()
        proxy.addSourceModel(self)
        proxy.addSourceModel(other)
        return proxy

    def check_index(
        self,
        index: QtCore.QModelIndex,
        index_is_valid: bool = False,
        do_not_use_parent: bool = False,
        parent_is_invalid: bool = False,
    ) -> bool:
        flag = QtCore.QAbstractItemModel.CheckIndexOption.NoOption
        if index_is_valid:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.IndexIsValid
        if do_not_use_parent:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.DoNotUseParent
        if parent_is_invalid:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.ParentIsInvalid
        check_flag = QtCore.QAbstractItemModel.CheckIndexOption(0) | flag
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
        rows_to_check: int = 5,
        role=constants.DISPLAY_ROLE,
    ) -> type | None:
        """Guess column data type by checking values of first rows with given role."""
        to_check = min(rows_to_check, self.rowCount())
        if to_check == 0:
            return None
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
    def remove_row(self, row: int, parent: QtCore.QModelIndex | None = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        self.beginRemoveRows(parent, row, row)
        yield None
        self.endRemoveRows()

    @contextlib.contextmanager
    def remove_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
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
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveColumns(parent, first, last)
        yield None
        self.endRemoveColumns()

    @contextlib.contextmanager
    def insert_row(self, row: int, parent: QtCore.QModelIndex | None = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        self.beginInsertRows(parent, row, row)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first or 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def append_rows(self, num_rows: int, parent: QtCore.QModelIndex | None = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        row_count = self.rowCount()
        self.beginInsertRows(parent, row_count, row_count + num_rows - 1)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_columns(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
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

    def get_role_names(self) -> dict[int, str]:
        return {i: v.data().decode() for i, v in self.roleNames().items()}

    def prefetch_tree(self, root_index: core.ModelIndex | None):
        for idx in self.iter_tree(root_index):
            if self.canFetchMore(idx):
                self.fetchMore(idx)

    def iter_tree(
        self,
        root_index: core.ModelIndex | None = None,
        depth: int | None = None,
    ) -> Iterator[core.ModelIndex]:
        """Iter through all indexes of the model tree."""
        if root_index is None:
            root_index = self.index(0, 0)
        if root_index.isValid():
            yield root_index
        if depth is not None:
            depth -= 1
            if depth == -1:
                return
        for i in range(self.rowCount(root_index)):
            idx = self.index(i, 0, root_index)
            yield from self.iter_tree(idx, depth)

    def search_tree(
        self,
        value: Any,
        role=constants.DISPLAY_ROLE,
        root_index: core.ModelIndex | None = None,
        max_results=None,
        depth: int | None = None,
    ) -> listdelegators.BaseListDelegator[core.ModelIndex]:
        """Search the tree for indexes with a given value in given role."""
        results = []
        # This makes it impossible to search for lists. I think thats fine.
        if not isinstance(value, list):
            value = [value]
        for idx in self.iter_tree(root_index, depth=depth):
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
        """
        indexes = [self.index(i, 0, index) for i in range(self.rowCount(index))]
        return listdelegators.BaseListDelegator(indexes)

    def get_index_key(self, index: core.ModelIndex):
        """Return a key for `index` from the source model into the _source_offset map.

        The key is a tuple of row indices on
        the path from the top if the model to the `index`.
        """
        key_path = []
        parent = index
        while parent.isValid():
            key_path.append(parent.row())
            parent = parent.parent()
        return tuple(reversed(key_path))

    def index_from_key(self, key_path: tuple[int, ...]):
        """Return a source QModelIndex for the given key."""
        model = self.sourceModel()
        if model is None:
            return core.ModelIndex()
        index = model.index(key_path[0], 0)
        for row in key_path[1:]:
            index = model.index(row, 0, index)
        return index


class AbstractItemModel(AbstractItemModelMixin, QtCore.QAbstractItemModel):
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
