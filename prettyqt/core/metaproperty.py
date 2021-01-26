from __future__ import annotations

from prettyqt.qt import QtCore


class MetaProperty:
    def __init__(self, metaproperty: QtCore.QMetaProperty):
        self.item = metaproperty

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return f"{type(self).__name__}({self.get_name()!r})"

    def get_name(self) -> str:
        return self.item.name()  # type: ignore


if __name__ == "__main__":
    from prettyqt import core

    metaobj = core.Object.get_metaobject()
