from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class MetaEnum:
    def __init__(self, metaenum: QtCore.QMetaEnum):
        self.item = metaenum

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __bool__(self):
        return self.item.isValid()

    def __getitem__(self, index: str | tuple[str, str]) -> int:
        if isinstance(index, str):
            result = self.item.keyToValue(index)[0]  # type: ignore
        else:
            val = "|".join(index)
            result = self.item.keysToValue(val)[0]  # type: ignore
        if result == -1:
            raise KeyError(index)
        return result  # type: ignore

    def __repr__(self):
        return get_repr(self, self.get_name())

    def __len__(self):
        return self.item.keyCount()

    def get_enum_name(self) -> str:
        return self.item.enumName()  # type: ignore

    def get_scope(self) -> str:
        return self.item.scope()  # type: ignore

    def get_name(self) -> str:
        return self.item.name()  # type: ignore


if __name__ == "__main__":
    from prettyqt import core

    metaobj = core.Object.get_static_metaobject()
