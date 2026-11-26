from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt.qt import QtCore

    _AbstractListModelBase = QtCore.QAbstractListModel
else:
    _AbstractListModelBase = object


class AbstractListModelMixin(core.AbstractItemModelMixin, _AbstractListModelBase):
    pass


class AbstractListModel(AbstractListModelMixin, core.QAbstractListModel):
    """Abstract model that can be subclassed to create one-dimensional list models."""
