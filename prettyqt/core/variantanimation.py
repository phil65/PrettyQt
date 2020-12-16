from typing import Callable, Union

from qtpy import QtCore

from prettyqt import core


QtCore.QVariantAnimation.__bases__ = (core.AbstractAnimation,)


class VariantAnimation(QtCore.QVariantAnimation):
    def __len__(self):
        return self.duration()

    def __getitem__(self, value: float):
        return self.keyValueAt(value)

    def __setitem__(self, key: float, value):
        self.setKeyValueAt(key, value)

    def set_easing(
        self, easing_type: Union[core.easingcurve.TypeStr, Callable[[float], float]]
    ):
        curve = core.EasingCurve()
        if isinstance(easing_type, str):
            curve.set_type(easing_type)
        else:
            curve.set_custom_type(easing_type)
        self.setEasingCurve(curve)

    def get_easing(self) -> Union[core.easingcurve.TypeStr, Callable[[float], float]]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        if typ == "custom":
            return curve.get_custom_type()
        else:
            return typ
