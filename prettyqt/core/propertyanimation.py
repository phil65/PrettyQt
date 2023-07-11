from __future__ import annotations

from collections.abc import Callable
from typing import Any

from prettyqt import core
from prettyqt.utils import datatypes


class PropertyAnimation(core.VariantAnimationMixin, core.QPropertyAnimation):
    """Animates Qt properties."""

    ID = "property"

    def __init__(self, *args, **kwargs):
        match args:
            case (core.QObject(), str(), *rest):
                super().__init__(args[0], bytes(args[1]), *rest, **kwargs)
            case _:
                super().__init__(*args, **kwargs)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"easingCurve": core.easingcurve.TYPE}
        return maps

    def apply_to(self, method: Callable):
        self.setTargetObject(method.__self__)
        self.set_property_name(method.__name__)

    def set_property_name(self, name: datatypes.ByteArrayType):
        name = datatypes.to_bytearray(name)
        self.setPropertyName(name)

    def get_property_name(self) -> str:
        return self.propertyName().data().decode()

    def get_property_value(self) -> Any:
        """Return the value of the property which should get animated."""
        prop_name = self.get_property_name()
        obj = self.targetObject()
        return obj.property(prop_name)


if __name__ == "__main__":
    anim = PropertyAnimation()
    anim.set_property_name("test")
