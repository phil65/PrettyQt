from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import classhelpers, get_repr


class MetaEnum:
    """Meta-data about an enumerator."""

    def __init__(self, metaenum: QtCore.QMetaEnum):
        self.item = metaenum

    def __getattr__(self, val):
        return getattr(self.item, val)

    def __bool__(self):
        return self.item.isValid()

    def __getitem__(self, index: str | tuple[str, str]) -> int:
        match index:
            case str():
                result = self.item.keyToValue(index)[0]  # type: ignore
            case (str(), str()):
                val = "|".join(index)
                result = self.item.keysToValue(val)[0]  # type: ignore
            case _:
                raise TypeError(index)
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

    def get_scope_object(self):
        scope = self.get_scope()
        return QtCore.Qt if scope == "Qt" else classhelpers.get_class_by_name(scope)

    def get_name(self) -> str:
        return self.item.name()  # type: ignore

    def list_options(self):
        return [self.value(i) for i in range(self.keyCount())]


if __name__ == "__main__":
    from prettyqt import widgets

    metaobj = widgets.AbstractItemView.get_static_metaobject()
    prop = metaobj.get_property("editTriggers")
    enumerator = prop.get_enumerator()
    print(enumerator)
    print(enumerator.get_scope_object())
