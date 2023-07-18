from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtQml
from prettyqt.utils import bidict, get_repr


PropertyTypeCategoryStr = Literal["invalid", "list", "object", "normal"]

PROPERTY_TYPE_CATEGORY = bidict(
    invalid=QtQml.QQmlProperty.PropertyTypeCategory.InvalidCategory,
    list=QtQml.QQmlProperty.PropertyTypeCategory.List,
    object=QtQml.QQmlProperty.PropertyTypeCategory.Object,
    normal=QtQml.QQmlProperty.PropertyTypeCategory.Normal,
)

TypeStr = Literal["invalid", "property", "signal_property"]

TYPE = bidict(
    invalid=QtQml.QQmlProperty.Type.Invalid,
    property=QtQml.QQmlProperty.Type.Property,
    signal_property=QtQml.QQmlProperty.Type.SignalProperty,
)


class QmlProperty(QtQml.QQmlProperty):
    """Abstracts accessing properties on objects created from QML."""

    def __repr__(self):
        return get_repr(self, self.object())

    def get_method(self) -> core.MetaMethod:
        return core.MetaMethod(self.method())

    def get_property(self) -> core.MetaProperty:
        return core.MetaProperty(self.property())

    def get_property_type_category(self) -> PropertyTypeCategoryStr:
        return PROPERTY_TYPE_CATEGORY.inverse[self.propertyTypeCategory()]

    def get_type(self) -> TypeStr:
        return TYPE.inverse[self.type()]


if __name__ == "__main__":
    prop = QmlProperty()
    method = prop.get_method()
    print(prop)
