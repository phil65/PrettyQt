from __future__ import annotations

from typing import Callable, Iterator, Tuple, Union

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import types


QtCore.QVariantAnimation.__bases__ = (core.AbstractAnimation,)


class VariantAnimation(QtCore.QVariantAnimation):
    def __getitem__(self, value: float) -> types.Variant:
        return self.keyValueAt(value)

    def __setitem__(self, key: float, value: types.Variant):
        self.setKeyValueAt(key, value)

    def __iter__(self) -> Iterator[Tuple[float, types.Variant]]:
        return iter(self.keyValues())

    def serialize_fields(self):
        return dict(
            duration=self.duration(),
            easing_curve=self.get_easing(),
            key_values=self.keyValues(),
        )

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

    def set_range(self, start, end):
        self.setStartValue(start)
        self.setEndValue(end)
