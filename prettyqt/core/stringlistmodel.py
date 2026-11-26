from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt.qt import QtCore

    _StringListModelBase = QtCore.QStringListModel
else:
    _StringListModelBase = object


class StringListModelMixin(core.AbstractListModelMixin, _StringListModelBase):
    pass


class StringListModel(StringListModelMixin, core.QStringListModel):
    """Model that supplies strings to views."""

    def __repr__(self):
        return f"{type(self).__name__}: ({self.rowCount()})"

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        # columnCount is private for StringListModel, but we need it
        # to avoid workarounds (for example in our Slice proxies).
        # So lets just return 1.
        return 1

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (str(), *_):
                return True
            case _:
                return False
