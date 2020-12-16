import contextlib
from typing import Optional

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


CHECK_INDEX_OPTIONS = bidict(
    none=QtCore.QAbstractItemModel.CheckIndexOption.NoOption,
    index_is_valid=QtCore.QAbstractItemModel.CheckIndexOption.IndexIsValid,
    do_not_use_parent=QtCore.QAbstractItemModel.CheckIndexOption.DoNotUseParent,
    parent_is_invalid=QtCore.QAbstractItemModel.CheckIndexOption.ParentIsInvalid,
)

LAYOUT_CHANGE_HINT = bidict(
    none=QtCore.QAbstractItemModel.NoLayoutChangeHint,
    vertical_sort=QtCore.QAbstractItemModel.VerticalSortHint,
    horizontal_sort=QtCore.QAbstractItemModel.HorizontalSortHint,
)


QtCore.QAbstractItemModel.__bases__ = (core.Object,)


class AbstractItemModel(QtCore.QAbstractItemModel):
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.rowCount()} rows"

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
        flag = QtCore.QAbstractItemModel.CheckIndexOptions(0)
        if index_is_valid:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.IndexIsValid
        if do_not_use_parent:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.DoNotUseParent
        if parent_is_invalid:
            flag |= QtCore.QAbstractItemModel.CheckIndexOption.ParentIsInvalid
        return self.checkIndex(index, flag)

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
        first: Optional[int] = None,
        last: Optional[int] = None,
        parent: Optional[QtCore.QModelIndex] = None,
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
        first: Optional[int] = None,
        last: Optional[int] = None,
        parent: Optional[QtCore.QModelIndex] = None,
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
        first: Optional[int] = None,
        last: Optional[int] = None,
        parent: Optional[QtCore.QModelIndex] = None,
    ):
        parent = QtCore.QModelIndex() if parent is None else parent
        first = first if first is not None else 0
        last = last if last is not None else self.rowCount()
        self.beginInsertRows(parent, first, last)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def append_rows(self, num_rows: int, parent: Optional[QtCore.QModelIndex] = None):
        parent = QtCore.QModelIndex() if parent is None else parent
        self.beginInsertRows(parent, self.rowCount(), self.rowCount() + num_rows - 1)
        yield None
        self.endInsertRows()

    @contextlib.contextmanager
    def insert_columns(
        self,
        first: Optional[int] = None,
        last: Optional[int] = None,
        parent: Optional[QtCore.QModelIndex] = None,
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
