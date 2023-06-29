# credits to Psygnal.

"""MutableSequence that emits events when altered.

Note For Developers
===================

Be cautious when re-implementing typical list-like methods here (e.g. extend,
pop, clear, etc...).  By not re-implementing those methods, we force ALL "CRUD"
(create, read, update, delete) operations to go through a few key methods
defined by the abc.MutableSequence interface, where we can emit the necessary
events.

Specifically:

- `insert` = "create" : add a new item/index to the list
- `__getitem__` = "read" : get the value of an existing index
- `__setitem__` = "update" : update the value of an existing index
- `__delitem__` = "delete" : remove an existing index from the list

All of the additional list-like methods are provided by the MutableSequence
interface, and call one of those 4 methods.  So if you override a method, you
MUST make sure that all the appropriate events are emitted.  (Tests should
cover this in test_evented_list.py)
"""
from __future__ import annotations

from collections.abc import Iterable, MutableSequence
from typing import Any, TypeVar, cast

from prettyqt import core


_T = TypeVar("_T")


class Signals(core.Object):
    inserting = core.Signal(int)  # idx
    inserted = core.Signal(int, object)  # (idx, value)
    removing = core.Signal(int)  # idx
    removed = core.Signal(int, object)  # (idx, value)
    moving = core.Signal(int, int)  # (src_idx, dest_idx)
    moved = core.Signal(int, int, object)  # (src_idx, dest_idx, value)
    changed = core.Signal(object, object, object)  # (int | slice, old, new)
    reordered = core.Signal()


class SignalList(MutableSequence[_T]):
    def __init__(
        self,
        data: Iterable[_T] = (),
        *,
        hashable: bool = True,
    ):
        super().__init__()
        self._data: list[_T] = []
        self._hashable = hashable
        self.signals = Signals()
        self.extend(data)

    def insert(self, index: int, value: _T) -> None:
        """Insert `value` before index."""
        _value = self._pre_insert(value)
        self.signals.inserting.emit(index)
        self._data.insert(index, _value)
        self.signals.inserted.emit(index, value)

    def __getitem__(self, key: int | slice) -> _T | SignalList[_T]:
        result = self._data[key]
        return self.__newlike__(result) if isinstance(result, list) else result

    def __setitem__(self, key: int | slice, value: _T | Iterable[_T]) -> None:
        old = self._data[key]
        if value is old:
            return
        if isinstance(key, slice):
            if not isinstance(value, Iterable):
                raise TypeError("Can only assign an iterable to slice")
            value = [self._pre_insert(v) for v in value]  # before we mutate the list
        else:
            value = self._pre_insert(cast("_T", value))
        self._data[key] = value
        self.signals.changed.emit(key, old, value)

    def __delitem__(self, key: int | slice) -> None:
        """Delete self[key]."""
        # delete from the end
        for parent, index in sorted(self._delitem_indices(key), reverse=True):
            parent.signals.removing.emit(index)
            item = parent._data.pop(index)
            self.signals.removed.emit(index, item)

    def _delitem_indices(self, key: int | slice) -> Iterable[tuple[SignalList[_T], int]]:
        # returning (self, int) allows subclasses to pass nested members
        match key:
            case int():
                yield (self, key if key >= 0 else key + len(self))
            case slice():
                yield from ((self, i) for i in range(*key.indices(len(self))))
            case _:
                raise TypeError(key)

    def _pre_insert(self, value: _T) -> _T:
        """Validate and or modify values prior to inserted."""
        return value

    def __newlike__(self, iterable: Iterable[_T]) -> SignalList[_T]:
        """Return new instance of same class."""
        return self.__class__(iterable)

    def copy(self) -> SignalList[_T]:
        """Return a shallow copy of the list."""
        return self.__newlike__(self)

    def __add__(self, other: Iterable[_T]) -> SignalList[_T]:
        """Add other to self, return new object."""
        copy = self.copy()
        copy.extend(other)
        return copy

    def __iadd__(self, other: Iterable[_T]) -> SignalList[_T]:
        """Add other to self in place (self += other)."""
        self.extend(other)
        return self

    def __radd__(self, other: list) -> list:
        """Reflected add (other + self).  Cast self to list."""
        return other + list(self)

    def __len__(self) -> int:
        """Return len(self)."""
        return len(self._data)

    def __repr__(self) -> str:
        """Return repr(self)."""
        return f"{type(self).__name__}({self._data})"

    def __eq__(self, other: Any) -> bool:
        """Return self==value."""
        return self._data == other

    def __hash__(self) -> int:
        """Return hash(self)."""
        # it's important to add this to allow this object to be hashable
        # given that we've also reimplemented __eq__
        if self._hashable:
            return id(self)
        name = self.__class__.__name__
        raise TypeError(f"unhashable type: {name!r}.")

    def reverse(self, *, emit_individual_events: bool = False) -> None:
        """Reverse list *IN PLACE*."""
        if emit_individual_events:
            super().reverse()
        else:
            self._data.reverse()
        self.signals.reordered.emit()

    def move(
        self, src_index: int, dest_index: int = 0, emit_reordered: bool = True
    ) -> bool:
        """Insert object at `src_index` before `dest_index`.

        Both indices refer to the list prior to any object removal (pre-move space).
        """
        if dest_index < 0:
            dest_index += len(self) + 1
        if dest_index in (src_index, src_index + 1):
            # this is a no-op
            return False

        self.signals.moving.emit(src_index, dest_index)
        item = self._data.pop(src_index)
        if dest_index > src_index:
            dest_index -= 1
        self._data.insert(dest_index, item)
        self.signals.moved.emit(src_index, dest_index, item)
        if emit_reordered:
            self.signals.reordered.emit()
        return True

    def move_multiple(self, sources: Iterable[int | slice], dest_index: int = 0) -> int:
        """Move a batch of `sources` indices, to a single destination.

        Note, if `dest_index` is higher than any of the `sources`, then
        the resulting position of the moved objects after the move operation
        is complete will be lower than `dest_index`.

        Arguments:
            sources:  A sequence of indices
            dest_index: The destination index. All sources will be inserted before this
                        index (in pre-move space), by default 0... which has the effect
                        of "bringing to front" everything in `sources`, or acting as a
                        "reorder" method if `sources` contains all indices.

        Returns:
            The number of successful move operations completed.

        Raises:
            TypeError
                If the destination index is a slice, or any of the source indices
                are not `int` or `slice`.
        """
        # calling list here makes sure that there are no index errors up front
        move_plan = list(self._move_plan(sources, dest_index))

        # don't assume index adjacency ... so move objects one at a time
        # this *could* be simplified with an intermediate list ... but this way
        # allows any views (such as QtViews) to update themselves more easily.
        # If this needs to be changed in the future for performance reasons,
        # then the associated QtListView will need to changed from using
        # `beginMoveRows` & `endMoveRows` to using `layoutAboutToBeChanged` &
        # `layoutChanged` while *manually* updating model indices with
        # `changePersistentIndexList`.  That becomes much harder to do with
        # nested tree-like models.
        for src, dest in move_plan:
            self.move(src, dest, emit_reordered=False)

        self.signals.reordered.emit()
        return len(move_plan)

    def _move_plan(
        self, sources: Iterable[int | slice], dest_index: int
    ) -> Iterable[tuple[int, int]]:
        """Yield prepared indices for a multi-move.

        Given a set of `sources` from anywhere in the list,
        and a single `dest_index`, this function computes and yields
        `(from_index, to_index)` tuples that can be used sequentially in
        single move operations.  It keeps track of what has moved where and
        updates the source and destination indices to reflect the model at each
        point in the process.

        This is useful for a drag-drop operation with a QtModel/View.

        Arguments:
            sources: An iterable of tuple[int] that should be moved to `dest_index`.
            dest_index: The destination for sources.
        """
        if isinstance(dest_index, slice):
            raise TypeError("Destination index may not be a slice")  # pragma: no cover

        to_move: list[int] = []
        for idx in sources:
            match idx:
                case slice():
                    to_move.extend(list(range(*idx.indices(len(self)))))
                case int():
                    to_move.append(idx)
                case _:
                    raise TypeError(idx)

        to_move = list(dict.fromkeys(to_move))

        if dest_index < 0:
            dest_index += len(self) + 1

        d_inc = 0
        popped: list[int] = []
        for i, src in enumerate(to_move):
            if src != dest_index:
                src -= sum(x <= src for x in popped)
                if src >= dest_index:
                    src += i
                yield src, dest_index + d_inc
            popped.append(src)
            if dest_index <= src:
                d_inc += 1


if __name__ == "__main__":
    import logging

    from prettyqt import debugging, widgets

    app = widgets.app()
    container = SignalList([0])
    with app.debug_mode():
        stalker = debugging.Stalker(container.signals, log_level=logging.DEBUG)
        stalker.hook()
        container.signals.changed.connect(print)
        container[0] = 2
        app.processEvents()
