from __future__ import annotations

from collections.abc import Sequence

from prettyqt import core


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
