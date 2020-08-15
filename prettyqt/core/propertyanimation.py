from qtpy import QtCore

from prettyqt import core

QtCore.QPropertyAnimation.__bases__ = (core.VariantAnimation,)


class PropertyAnimation(QtCore.QPropertyAnimation):
    def apply_to(self, object: QtCore.QObject, attribute: str):
        self.setTargetObject(object)
        self.setPropertyName(str.encode(attribute))
