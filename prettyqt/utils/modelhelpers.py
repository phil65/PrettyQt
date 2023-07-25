from __future__ import annotations

from collections.abc import Callable, Sequence
import functools

from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt import widgets


def is_descendent_of(
    indexes: list[core.ModelIndex] | core.QItemSelection | core.QItemSelectionRange,
    index: core.ModelIndex,
) -> bool:
    if not index.isValid():
        return False
    match indexes:
        case list():
            if index in indexes:
                return False
            while (index := index.parent()).isValid():
                if index in indexes:
                    return True
            return False
        case core.QItemSelection() | core.QItemSelectionRange():
            if indexes.contains(index):
                return False
            while (index := index.parent()).isValid():
                if indexes.contains(index):
                    return True
            return False
        case _:
            raise TypeError(indexes)


def find_root_index(index: core.ModelIndex) -> core.ModelIndex:
    while index.parent().isValid():
        index = index.parent()
    return index


def get_parent_indexes(index: core.ModelIndex) -> list[core.ModelIndex]:
    indexes = []
    while index.isValid():
        indexes.insert(0, index)
        index = index.parent()
    return indexes


def get_proxy_chain(model: core.QAbstractItemModel) -> list[core.QAbstractItemModel]:
    models = [model]
    while isinstance(model, core.QAbstractProxyModel):
        model = model.sourceModel()
        models.append(model)
    return models


def index_from_key(
    model: core.QAbstractItemModel,
    key_path: Sequence[tuple[int, int] | int],
    parent_index: core.ModelIndex,
) -> core.ModelIndex:
    if model is None:
        return core.ModelIndex()
    index = parent_index or core.ModelIndex()
    for key in key_path:
        key = (key, 0) if isinstance(key, int) else key
        index = model.index(*key, index)
    return index


def ci(
    index_is_valid: bool = False,
    do_not_use_parent: bool = False,
    parent_is_invalid: bool = False,
):
    def inner(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(
            ref: core.AbstractItemModelMixin, index: core.QModelIndex, *args, **kwargs
        ):
            if ref.check_index(
                index, index_is_valid, do_not_use_parent, parent_is_invalid
            ):
                return fn(ref, index, *args, **kwargs)
            else:
                raise TypeError("Invalid index")

        return wrapper

    return inner


def requires_model(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapper(ref: widgets.AbstractItemViewMixin, *args, **kwargs):
        if ref.model() is None:
            raise RuntimeError(f"Trying to call {fn.__name__} without a model set.")
        return fn(ref, *args, **kwargs)

    return wrapper
