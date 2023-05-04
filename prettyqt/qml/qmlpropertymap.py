from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQml
from prettyqt.utils import datatypes, get_repr


class QmlPropertyMapMixin(core.ObjectMixin):
    pass


class QmlPropertyMap(QmlPropertyMapMixin, QtQml.QQmlPropertyMap):
    def __repr__(self):
        return get_repr(self, self.as_dict())

    def __setitem__(self, key: str, value: datatypes.Variant):
        self.insert(key, value)

    def __getitem__(self, key: str) -> datatypes.Variant:
        return self.value(key)

    def __delitem__(self, key: str):
        self.clear(key)

    def __contains__(self, key):
        return self.contains(key)

    def __bool__(self):
        return not self.isEmpty()

    def __iter__(self):
        return iter(self.as_dict())

    def items(self):
        return self.as_dict().items()

    def as_dict(self) -> dict[str, datatypes.Variant]:
        return {i: self.value(i) for i in self.keys()}


if __name__ == "__main__":
    propmap = QmlPropertyMap()
    propmap["a"] = 2
