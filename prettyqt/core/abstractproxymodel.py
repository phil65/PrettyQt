from __future__ import annotations

from collections.abc import Callable, Generator, Sequence
import logging

from typing import Any

from prettyqt import core, qt
from prettyqt.utils import modelhelpers


logger = logging.getLogger(__name__)


class AbstractProxyModelMixin(core.AbstractItemModelMixin):
    ID = ""
    ICON = "mdi.table-edit"

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        yield f"{type(self).__name__}("
        yield 1
        # yield 1
        yield f"objectName={self.objectName()}"
        yield 0
        for k, v in self.get_properties(include_super=False).items():
            yield f"{k}={v!r}"
            yield 0
        model = self.sourceModel()
        if hasattr(model, "__pretty__"):
            yield from model.__pretty__(fmt, **kwargs)
            yield 0
        yield -1
        # yield -1
        yield ")"

    def parent(self, *args):
        # workaround: PyQt6 QIdentityproxymodel.parent() missing
        if not args and qt.API == "pyqt6":
            return core.QAbstractProxyModel.parent(self)
        return super().parent(*args)

    def first_item_index(self) -> core.ModelIndex:
        """Return the first child of the root item."""
        # We cannot just call the same function of the source model because the first node
        # there may be hidden.
        proxy_root_index = self.mapFromSource(core.ModelIndex())
        return self.index(0, 0, proxy_root_index)

    def get_source_model(self, skip_proxies: bool = True):
        model = self.sourceModel()
        if skip_proxies:
            while isinstance(model, core.QAbstractProxyModel):
                model = model.sourceModel()
        return model

    def remove(self):
        parent = self.parent()
        models = parent.get_models()
        idx = models.index(self)
        if idx == len(models) - 1:
            parent.set_model(models[idx - 1])
            self.setSourceModel(None)
        elif idx == 0 and len(models) > 0:
            parent.set_model(models[1])
        elif idx > 0 and len(models) > 2:
            models[idx - 1].setSourceModel(models[idx + 1])
            self.setSourceModel(None)

    def get_source_mapping(self, leaves_only: bool = False):
        _source_key = []
        _source_offset = {}
        source = self.sourceModel()

        def create_mapping(
            model,
            index: core.ModelIndex,
            key_path: tuple[int, ...],
            leaves_only: bool = False,
        ):
            if (rowcount := model.rowCount(index)) > 0:
                if not leaves_only:
                    _source_offset[key_path] = len(_source_offset)
                    _source_key.append(key_path)
                for i in range(rowcount):
                    child = model.index(i, 0, index)
                    create_mapping(model, child, (*key_path, i), leaves_only=leaves_only)
            else:
                _source_offset[key_path] = len(_source_offset)
                _source_key.append(key_path)

        for i in range(source.rowCount()):
            create_mapping(source, source.index(i, 0), (i,), leaves_only=leaves_only)
        return _source_key, _source_offset

    def source_index_from_key(
        self,
        key_path: Sequence[tuple[int, int] | int],
        parent_index: core.ModelIndex | None = None,
    ) -> core.ModelIndex:
        """Return a QModelIndex of the sourceModel for the given key.

        Arguments:
            key_path: Key path to get an index for.
                      Should be a sequence of either (row, column)  or row indices
            parent_index: ModelIndex to start indexing from. Defaults to root index.
        """
        model = self.sourceModel()
        return modelhelpers.index_from_key(model, key_path, parent_index)


class AbstractProxyModel(AbstractProxyModelMixin, core.QAbstractProxyModel):
    """Base class for proxy item models that can do sorting, filtering and processing."""


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    table = widgets.TableView()
    model = widgets.FileSystemModel(parent=table)
    table.set_model(model)
