from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import get_repr


class MetaProperty:
    """Meta-data about a property."""

    def __init__(self, metaproperty: core.QMetaProperty):
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

    def get_python_type(self) -> type:
        return self.get_meta_type().get_type()

    def get_notify_signal(self) -> core.MetaMethod | None:
        if (signal := self.notifySignal()).isValid():
            return core.MetaMethod(signal)
        return None

    def get_enumerator(self) -> core.MetaEnum | None:
        if (enumerator := self.enumerator()).isValid():
            return core.MetaEnum(enumerator)
        return None

    def get_enumerator_type(self) -> Literal["flag", "enum"] | None:
        if self.isFlagType():
            return "flag"
        if self.isEnumType():
            return "enum"
        return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    metaobj = widget.get_metaobject()
    prop = metaobj.get_property("x")
    value = prop.read(widget)
