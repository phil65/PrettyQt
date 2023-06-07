from __future__ import annotations

from collections.abc import Callable, Iterator

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import datatypes


class VariantAnimationMixin(core.AbstractAnimationMixin):
    def __getitem__(self, value: float) -> datatypes.Variant:
        return self.keyValueAt(value)

    def __setitem__(self, key: float, value: datatypes.Variant):
        self.setKeyValueAt(key, value)

    def __iter__(self) -> Iterator[tuple[float, datatypes.Variant]]:
        return iter(self.keyValues())

    def set_easing(
        self, easing_type: core.easingcurve.TypeStr | Callable[[float], float]
    ):
        curve = core.EasingCurve()
        if isinstance(easing_type, str):
            curve.set_type(easing_type)
        else:
            curve.set_custom_type(easing_type)
        self.setEasingCurve(curve)

    def get_easing(self) -> core.easingcurve.TypeStr | Callable[[float], float]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        return curve.get_custom_type() if typ == "custom" else typ

    def set_range(self, start, end):
        self.setStartValue(start)
        self.setEndValue(end)


class VariantAnimation(VariantAnimationMixin, QtCore.QVariantAnimation):
    pass
