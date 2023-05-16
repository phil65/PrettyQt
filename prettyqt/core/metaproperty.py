from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class MetaProperty:
    def __init__(self, metaproperty: QtCore.QMetaProperty):
        self.item = metaproperty

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return get_repr(self, self.get_name())

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_name(self) -> str:
        return self.item.name()  # type: ignore

    def get_meta_type(self) -> core.MetaType:
        return core.MetaType(self.metaType().id())

    def get_notify_signal(self) -> core.MetaMethod:
        return core.MetaMethod(self.notifySignal())

    def get_enumerator(self) -> core.MetaEnum:
        return core.MetaEnum(self.enumerator())


if __name__ == "__main__":
    metaobj = core.Object.get_static_metaobject()
