from __future__ import annotations

from typing import Callable, Literal

from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


TYPE = bidict(
    linear=QtCore.QEasingCurve.Type.Linear,
    in_quad=QtCore.QEasingCurve.Type.InQuad,
    out_quad=QtCore.QEasingCurve.Type.OutQuad,
    in_out_quad=QtCore.QEasingCurve.Type.InOutQuad,
    out_in_quad=QtCore.QEasingCurve.Type.OutInQuad,
    in_cubic=QtCore.QEasingCurve.Type.InCubic,
    out_cubic=QtCore.QEasingCurve.Type.OutCubic,
    in_out_cubic=QtCore.QEasingCurve.Type.InOutCubic,
    out_in_cubic=QtCore.QEasingCurve.Type.OutInCubic,
    in_quart=QtCore.QEasingCurve.Type.InQuart,
    out_quart=QtCore.QEasingCurve.Type.OutQuart,
    in_out_quart=QtCore.QEasingCurve.Type.InOutQuart,
    out_in_quart=QtCore.QEasingCurve.Type.OutInQuart,
    in_quint=QtCore.QEasingCurve.Type.InQuint,
    out_quint=QtCore.QEasingCurve.Type.OutQuint,
    in_out_quint=QtCore.QEasingCurve.Type.InOutQuint,
    out_in_quint=QtCore.QEasingCurve.Type.OutInQuint,
    in_sine=QtCore.QEasingCurve.Type.InSine,
    out_sine=QtCore.QEasingCurve.Type.OutSine,
    in_out_sine=QtCore.QEasingCurve.Type.InOutSine,
    out_in_sine=QtCore.QEasingCurve.Type.OutInSine,
    in_expo=QtCore.QEasingCurve.Type.InExpo,
    out_expo=QtCore.QEasingCurve.Type.OutExpo,
    in_out_expo=QtCore.QEasingCurve.Type.InOutExpo,
    out_in_expo=QtCore.QEasingCurve.Type.OutInExpo,
    in_circ=QtCore.QEasingCurve.Type.InCirc,
    out_circ=QtCore.QEasingCurve.Type.OutCirc,
    in_out_circ=QtCore.QEasingCurve.Type.InOutCirc,
    out_in_circ=QtCore.QEasingCurve.Type.OutInCirc,
    in_elastic=QtCore.QEasingCurve.Type.InElastic,
    out_elastic=QtCore.QEasingCurve.Type.OutElastic,
    in_out_elastic=QtCore.QEasingCurve.Type.InOutElastic,
    out_in_elastic=QtCore.QEasingCurve.Type.OutInElastic,
    in_back=QtCore.QEasingCurve.Type.InBack,
    out_back=QtCore.QEasingCurve.Type.OutBack,
    in_out_back=QtCore.QEasingCurve.Type.InOutBack,
    out_in_back=QtCore.QEasingCurve.Type.OutInBack,
    in_bounce=QtCore.QEasingCurve.Type.InBounce,
    out_bounce=QtCore.QEasingCurve.Type.OutBounce,
    in_out_bounce=QtCore.QEasingCurve.Type.InOutBounce,
    out_in_bounce=QtCore.QEasingCurve.Type.OutInBounce,
    bezier_spline=QtCore.QEasingCurve.Type.BezierSpline,
    tcb_spline=QtCore.QEasingCurve.Type.TCBSpline,
    custom=QtCore.QEasingCurve.Type.Custom,
)

TypeStr = Literal[
    "linear",
    "in_quad",
    "out_quad",
    "in_out_quad",
    "out_in_quad",
    "in_cubic",
    "out_cubic",
    "in_out_cubic",
    "out_in_cubic",
    "in_quart",
    "out_quart",
    "in_out_quart",
    "out_in_quart",
    "in_quint",
    "out_quint",
    "in_out_quint",
    "out_in_quint",
    "in_sine",
    "out_sine",
    "in_out_sine",
    "out_in_sine",
    "in_expo",
    "out_expo",
    "in_out_expo",
    "out_in_expo",
    "in_circ",
    "out_circ",
    "in_out_circ",
    "out_in_circ",
    "in_elastic",
    "out_elastic",
    "in_out_elastic",
    "out_in_elastic",
    "in_back",
    "out_back",
    "in_out_back",
    "out_in_back",
    "in_bounce",
    "out_bounce",
    "in_out_bounce",
    "out_in_bounce",
    "bezier_spline",
    "tcb_spline",
    "custom",
]
CurveMethod = Callable[[float], float]


class EasingCurve(QtCore.QEasingCurve):
    def __init__(self, other_or_type: TypeStr | int | QtCore.QEasingCurve = "linear"):
        if isinstance(other_or_type, str) and other_or_type in TYPE:
            typ = TYPE[other_or_type]
        else:
            typ = other_or_type
        super().__init__(typ)

    def __getitem__(self, value: float) -> float:
        return self.valueForProgress(value)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_type()!r})"

    def set_custom_type(self, method: CurveMethod):
        self.setCustomType(method)

    def get_custom_type(self) -> CurveMethod:
        return self.customType()  # type: ignore

    def set_type(self, typ: TypeStr):
        """Set easing curve type.

        Args:
            typ: easing curve type

        Raises:
            InvalidParamError: easing curve type does not exist
        """
        if typ not in TYPE:
            raise InvalidParamError(typ, TYPE)
        self.setType(TYPE[typ])

    def get_type(self) -> TypeStr:
        """Get the current easing curve type.

        Returns:
            easing curve type
        """
        return TYPE.inverse[self.type()]


if __name__ == "__main__":
    c = EasingCurve()
    print(repr(c))
