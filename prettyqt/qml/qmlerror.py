from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQml
from prettyqt.utils import get_repr


class QmlError(QtQml.QQmlError):
    def __repr__(self):
        return get_repr(self, self.toString())

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def get_property(self) -> core.MetaProperty:
        return core.MetaProperty(self.property())

    def __str__(self):
        return self.toString()


if __name__ == "__main__":
    error = QmlError()
