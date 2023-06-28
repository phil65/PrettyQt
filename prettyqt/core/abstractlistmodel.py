from __future__ import annotations

from prettyqt import core


class AbstractListModelMixin(core.AbstractItemModelMixin):
    pass


class AbstractListModel(AbstractListModelMixin, core.QAbstractListModel):
    pass
