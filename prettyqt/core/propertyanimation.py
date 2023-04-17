from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class PropertyAnimation(core.VariantAnimationMixin, QtCore.QPropertyAnimation):
    def apply_to(self, obj: QtCore.QObject, attribute: str):
        self.setTargetObject(obj)
        self.set_property_name(attribute)

    def set_property_name(self, name: datatypes.ByteArrayType):
        if isinstance(name, str):
            name = name.encode()
        if isinstance(name, bytes):
            name = QtCore.QByteArray(name)
        self.setPropertyName(name)

    def get_property_name(self) -> str:
        return bytes(self.propertyName()).decode()


if __name__ == "__main__":
    anim = PropertyAnimation()
    anim.set_property_name("test")
