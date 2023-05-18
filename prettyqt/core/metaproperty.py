from __future__ import annotations

from typing import Literal

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
        return core.MetaType(self.userType())  # same as self.metaType().id()

    def get_notify_signal(self) -> core.MetaMethod:
        return core.MetaMethod(self.notifySignal())

    def get_enumerator(self) -> core.MetaEnum:
        return core.MetaEnum(self.enumerator())

    def get_enumerator_type(self) -> Literal["flag", "enum"] | None:
        if self.isFlagType():
            return "flag"
        elif self.isEnumType():
            return "enum"
        else:
            return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    metaobj = widget.get_metaobject()
    prop = metaobj.get_property("windowModality")
    value = prop.read(widget)
    print(type(value), value)
