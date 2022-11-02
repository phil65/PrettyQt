from __future__ import annotations

import contextlib

from prettyqt import core, qt
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


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


QtCore.QAbstractItemModel.__bases__ = (core.Object,)


class AbstractItemModel(QtCore.QAbstractItemModel):
    def __repr__(self):
        return f"{type(self).__name__}: {self.rowCount()} rows"

    def __len__(self) -> int:
        """Return amount of rows."""
        return self.rowCount()

    # causes issues with PySide2
    # def __getitem__(self, index: Tuple[int, int]) -> QtCore.QModelIndex:
    #     return self.index(*index)

    def check_index(
        self,
        index: QtCore.QModelIndex,
        index_is_valid: bool = False,
        do_not_use_parent: bool = False,
        parent_is_invalid: bool = False,
    ) -> bool:
        flag = QtCore.QAbstractItemModel.CheckIndexOption.NoOption
        if index_is_valid:
            flag |= CHECK_INDEX_OPTIONS["index_is_valid"]  # type: ignore
        if do_not_use_parent:
            flag |= CHECK_INDEX_OPTIONS["do_not_use_parent"]  # type: ignore
        if parent_is_invalid:
            flag |= CHECK_INDEX_OPTIONS["parent_is_invalid"]  # type: ignore
        check_flag = QtCore.QAbstractItemModel.CheckIndexOption(0) | flag  # type: ignore
        if qt.API.endswith("5"):
            check_flag = QtCore.QAbstractItemModel.CheckIndexOptions(check_flag)
        return self.checkIndex(index, check_flag)  # type: ignore

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

    def update_row(self, row: int):
        start_index = self.index(row, 0)
        end_index = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(start_index, end_index)

    @contextlib.contextmanager
    def remove_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
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
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginRemoveColumns(parent, first, last)
        yield None
        self.endRemoveColumns()

    @contextlib.contextmanager
    def insert_rows(
        self,
        first: int | None = None,
        last: int | None = None,
        parent: QtCore.QModelIndex | None = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def append_rows(self, num_rows: int, parent: QtCore.QModelIndex | None = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        self.beginInsertRows(parent, self.rowCount(), self.rowCount() + num_rows - 1)
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
        first = first if first is not None else 0
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
