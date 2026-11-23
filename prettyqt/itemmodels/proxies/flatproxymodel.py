from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    _Base = core.QAbstractProxyModel
else:
    _Base = object


class FlatProxyMixin(_Base):
    """Mixin for proxies which reshape a source table into another flat table.

    Provides index() / parent() for a flat (non-hierarchical) model and resets the
    proxy whenever the source model changes, since any source change may reshape the
    whole proxy. (No signals of the source get forwarded "as-is", which also makes it
    possible to use this mixin together with QIdentityProxyModel subclasses.)

    Subclasses need to implement rowCount, columnCount, data, mapToSource
    and mapFromSource.
    The `_update_cache` hook gets called on every reset, subclasses can use it to
    recompute cached mappings.
    """

    def setSourceModel(self, model: core.QAbstractItemModel):
        if (old := self.sourceModel()) is not None:
            for signal in self._structure_signals(old):
                signal.disconnect(self._on_source_changed)
        self.beginResetModel()
        # Explicitly use the QAbstractProxyModel implementation, this way
        # QIdentityProxyModel does not connect its signal forwarding.
        core.QAbstractProxyModel.setSourceModel(self, model)
        self._update_cache()
        self.endResetModel()
        if model is not None:
            for signal in self._structure_signals(model):
                signal.connect(self._on_source_changed)

    @staticmethod
    def _structure_signals(model: core.QAbstractItemModel):
        return [
            model.rowsInserted,
            model.rowsRemoved,
            model.rowsMoved,
            model.columnsInserted,
            model.columnsRemoved,
            model.columnsMoved,
            model.modelReset,
            model.layoutChanged,
            model.headerDataChanged,
            # values can affect the shape (for example for unmelt), so we reset.
            model.dataChanged,
        ]

    def _update_cache(self):
        """Hook to recompute cached data, called on every source change."""

    def _on_source_changed(self, *_args):
        self.beginResetModel()
        self._update_cache()
        self.endResetModel()

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        if parent.isValid() or not self.hasIndex(row, column, parent):
            return core.ModelIndex()
        return self.createIndex(row, column)

    def parent(self, *args) -> core.ModelIndex | core.QObject | None:
        if not args:  # QObject.parent()
            return core.QObject.parent(self)
        return core.ModelIndex()

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.isValid():
            return False
        return self.rowCount() > 0 and self.columnCount() > 0

    def sibling(self, row: int, column: int, idx: core.ModelIndex) -> core.ModelIndex:
        return self.index(row, column)


class FlatProxyModel(FlatProxyMixin, core.AbstractProxyModel):
    """Base class for proxies which reshape a source table into another flat table."""
