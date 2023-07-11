from __future__ import annotations

from collections.abc import Callable, Iterator

from typing_extensions import Self

from prettyqt import core
from prettyqt.utils import datatypes


class VariantAnimationMixin(core.AbstractAnimationMixin):
    def __getitem__(self, value: float) -> datatypes.Variant:
        return self.keyValueAt(value)

    def __setitem__(self, key: float, value: datatypes.Variant):
        self.setKeyValueAt(key, value)

    def __iter__(self) -> Iterator[tuple[float, datatypes.Variant]]:
        return iter(self.keyValues())

    def set_easing(
        self,
        easing_type: core.easingcurve.TypeStr
        | core.QEasingCurve.Type
        | Callable[[float], float],
    ):
        curve = core.EasingCurve()
        if callable(easing_type):
            curve.set_custom_type(easing_type)
        else:
            curve.set_type(easing_type)
        self.setEasingCurve(curve)

    def get_easing(self) -> core.easingcurve.TypeStr | Callable[[float], float]:
        curve = core.EasingCurve(self.easingCurve())
        typ = curve.get_type()
        return curve.get_custom_type() if typ == "custom" else typ

    def set_range(self, start, end):
        self.setStartValue(start)
        self.setEndValue(end)

    def reverse(self):
        """True reverse instead of just setting direction."""
        self.setKeyValues(list(reversed(self.keyValues())))

    def reversed(self) -> VariantAnimation:
        """Return a reversed copy of the animation."""
        new = self.get_metaobject().copy(self)
        new.reverse()
        return new

    def append_reversed(self) -> Self:
        """Append the reversed animation, effectively doubling the duration."""
        self.setDuration(self.duration() * 2)
        first_part = [(k / 2, v) for k, v in self.keyValues()]
        second_part = [(1 - (k / 2), v) for k, v in self.keyValues()]
        keys = first_part + list(reversed(second_part))[1:]
        self.setKeyValues(keys)
        return self


class VariantAnimation(VariantAnimationMixin, core.QVariantAnimation):
    """Base class for animations."""


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    anim = VariantAnimation()
    anim.set_start_value(10)
    anim = anim.reversed()
    anim.run()
    print(anim.endValue())
