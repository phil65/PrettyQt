from __future__ import annotations

from collections.abc import Callable

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class PropertyAnimation(core.VariantAnimationMixin, QtCore.QPropertyAnimation):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"easingCurve": core.easingcurve.TYPE}
        return maps

    def apply_to(self, method: Callable):
        self.setTargetObject(method.__self__)
        self.set_property_name(method.__name__)

    def set_property_name(self, name: datatypes.ByteArrayType):
        if isinstance(name, str):
            name = name.encode()
        if isinstance(name, bytes):
            name = QtCore.QByteArray(name)
        self.setPropertyName(name)

    def get_property_name(self) -> str:
        return self.propertyName().data().decode()


if __name__ == "__main__":
    anim = PropertyAnimation()
    anim.set_property_name("test")
