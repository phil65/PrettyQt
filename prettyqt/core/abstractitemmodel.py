from __future__ import annotations

from collections.abc import Callable
import contextlib
import logging
from typing import Any, Literal

from collections.abc import Iterator

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import bidict, helpers


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

ProxyStr = Literal[
    "fuzzy",
    "transpose",
    "sort_filter",
    "identity",
    "value_transformation",
    "range_filter",
    "checkable",
    "subset",
    "flatten_tree",
    "table_to_list",
    "predicate_filter",
    "size_limiter",
    "subsequence",
    "appearance",
    "column_join",
    "read_only",
]


class Proxyfier:
    def __init__(self, model):
        self._model = model

    def __getitem__(self, index):
        parent = self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")

        from prettyqt import custom_models

        match index:
            case (arg_1, arg_2):
                kwargs = dict(row_filter=arg_1, column_filter=arg_2, parent=parent)
            case _:
                kwargs = dict(row_filter=index, column_filter=None, parent=parent)
        proxy = proxy = custom_models.SubsetFilterProxyModel(**kwargs)
        proxy.setSourceModel(self._model)
        return proxy

    def transpose(
        self, parent: QtWidgets.QWidget | None = None
    ) -> core.TransposeProxyModel:
        # PySide6 needs widget parent here
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")
        proxy = core.TransposeProxyModel(parent=parent)
        proxy.setSourceModel(self._model)
        return proxy

    def modify(
        self,
        fn: Callable[[Any], Any],
        column: int | None = None,
        row: int | None = None,
        role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
        selector: Callable[[Any], bool] | None = None,
        selector_role: QtCore.Qt.ItemDataRole = constants.DISPLAY_ROLE,
        parent: QtWidgets.QWidget | None = None,
    ):
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")

        from prettyqt import custom_models

        proxy = custom_models.ValueTransformationProxyModel(parent=parent)
        proxy.add_transformer(fn, column, row, role, selector, selector_role)
        proxy.setSourceModel(self._model)
        return proxy

    def get_proxy(
        self, proxy: ProxyStr, parent: QtWidgets.QWidget | None = None, **kwargs
    ):
        parent = parent or self._model.parent()
        if parent is None:
            raise ValueError("needs parent!")
        Klass = helpers.get_class_for_id(core.AbstractProxyModelMixin, proxy)
        proxy = Klass(parent=parent, **kwargs)
        proxy.setSourceModel(self._model)
        return proxy


class AbstractItemModelMixin(core.ObjectMixin):
    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED | constants.IS_ENABLED | constants.IS_SELECTABLE
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxifier = Proxyfier(self)

    def __repr__(self):
        return f"{type(self).__name__}: ({self.rowCount()}, {self.columnCount()})"

    def __len__(self) -> int:
        """Return amount of rows."""
        return self.rowCount()

    def __add__(
        self, other: QtCore.QAbstractItemModel
    ) -> core.ConcatenateTablesProxyModel:
        proxy = core.ConcatenateTablesProxyModel()
        proxy.addSourceModel(self)
        proxy.addSourceModel(other)
        return proxy

    @classmethod
    def ci(
        cls,
        index_is_valid: bool = False,
        do_not_use_parent: bool = False,
        parent_is_invalid: bool = False,
    ):
        def inner(method):
            def wrapper(
                ref: AbstractItemModelMixin, index: QtCore.QModelIndex, *args, **kwargs
            ):
                if ref.check_index(
                    index, index_is_valid, do_not_use_parent, parent_is_invalid
                ):
                    return method(ref, index, *args, **kwargs)
                else:
                    raise TypeError("Invalid index")

            return wrapper

        return inner

    def check_index(
        self,
        index: QtCore.QModelIndex,
        index_is_valid: bool = False,
        do_not_use_parent: bool = False,
        parent_is_invalid: bool = False,
    ) -> bool:
        flag = QtCore.QAbstractItemModel.CheckIndexOption.NoOption
        if index_is_valid:
            flag |= CHECK_INDEX_OPTIONS["index_is_valid"]
        if do_not_use_parent:
            flag |= CHECK_INDEX_OPTIONS["do_not_use_parent"]
        if parent_is_invalid:
            flag |= CHECK_INDEX_OPTIONS["parent_is_invalid"]
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

    def iter_tree(
        self, root_index: core.ModelIndex | None = None
    ) -> Iterator[core.ModelIndex]:
        if root_index is None:
            root_index = self.index(0, 0)
        if root_index.isValid():
            yield root_index
        for i in range(self.rowCount(root_index)):
            idx = self.index(i, 0, root_index)
            yield from self.iter_tree(idx)

    def search_tree(
        self,
        value: Any,
        role=constants.DISPLAY_ROLE,
        root_index: core.ModelIndex | None = None,
    ) -> Any:
        if root_index is None:
            root_index = self.index(0, 0)
        if self.data(root_index, role) == value:
            return root_index
        for i in range(self.rowCount(root_index)):
            idx = self.index(i, 0, root_index)
            self.search_tree(value, role, idx)
        return None


class AbstractItemModel(AbstractItemModelMixin, QtCore.QAbstractItemModel):
    pass
