from qtpy import QtCore

from prettyqt import core


QtCore.QPropertyAnimation.__bases__ = (core.VariantAnimation,)


class PropertyAnimation(QtCore.QPropertyAnimation):
    def apply_to(self, obj: QtCore.QObject, attribute: str):
        self.setTargetObject(obj)
        self.set_property_name(attribute)

    def set_property_name(self, name: str):
        self.setPropertyName(name.encode())

    def get_property_name(self) -> str:
        return bytes(self.propertyName()).decode()


if __name__ == "__main__":
    anim = PropertyAnimation()
    anim.set_property_name("test")
