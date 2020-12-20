from typing import Union

from qtpy import QtCore

from prettyqt import core


QtCore.QPropertyAnimation.__bases__ = (core.VariantAnimation,)


class PropertyAnimation(QtCore.QPropertyAnimation):
    def apply_to(self, obj: QtCore.QObject, attribute: str):
        self.setTargetObject(obj)
        self.set_property_name(attribute)

    def set_property_name(self, name: Union[str, bytes, QtCore.QByteArray]):
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
