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

    def reverse(self):
        old_start = self.startValue()
        old_end = self.endValue()
        self.setStartValue(old_end)
        self.setEndValue(old_start)

    def reversed(self) -> VariantAnimation:
        new = self.get_metaobject().copy(self)
        new.reverse()
        return new

    def append_reversed(self) -> core.SequentialAnimationGroup:
        revers = self.reversed()
        animation = core.SequentialAnimationGroup()
        animation.addAnimation(self)
        animation.addAnimation(revers)
        return animation


class VariantAnimation(VariantAnimationMixin, QtCore.QVariantAnimation):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    anim = VariantAnimation()
    anim.set_start_value(10)
    anim = anim.reversed()
    anim.run()
    print(anim.endValue())
