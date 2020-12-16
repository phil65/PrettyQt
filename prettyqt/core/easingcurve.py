from typing import Callable, Literal, Union

from qtpy import QtCore

from prettyqt.utils import InvalidParamError, bidict


TYPE = bidict(
    linear=QtCore.QEasingCurve.Linear,
    in_quad=QtCore.QEasingCurve.InQuad,
    out_quad=QtCore.QEasingCurve.OutQuad,
    in_out_quad=QtCore.QEasingCurve.InOutQuad,
    out_in_quad=QtCore.QEasingCurve.OutInQuad,
    in_cubic=QtCore.QEasingCurve.InCubic,
    out_cubic=QtCore.QEasingCurve.OutCubic,
    in_out_cubic=QtCore.QEasingCurve.InOutCubic,
    out_in_cubic=QtCore.QEasingCurve.OutInCubic,
    in_quart=QtCore.QEasingCurve.InQuart,
    out_quart=QtCore.QEasingCurve.OutQuart,
    in_out_quart=QtCore.QEasingCurve.InOutQuart,
    out_in_quart=QtCore.QEasingCurve.OutInQuart,
    in_quint=QtCore.QEasingCurve.InQuint,
    out_quint=QtCore.QEasingCurve.OutQuint,
    in_out_quint=QtCore.QEasingCurve.InOutQuint,
    out_in_quint=QtCore.QEasingCurve.OutInQuint,
    in_sine=QtCore.QEasingCurve.InSine,
    out_sine=QtCore.QEasingCurve.OutSine,
    in_out_sine=QtCore.QEasingCurve.InOutSine,
    out_in_sine=QtCore.QEasingCurve.OutInSine,
    in_expo=QtCore.QEasingCurve.InExpo,
    out_expo=QtCore.QEasingCurve.OutExpo,
    in_out_expo=QtCore.QEasingCurve.InOutExpo,
    out_in_expo=QtCore.QEasingCurve.OutInExpo,
    in_circ=QtCore.QEasingCurve.InCirc,
    out_circ=QtCore.QEasingCurve.OutCirc,
    in_out_circ=QtCore.QEasingCurve.InOutCirc,
    out_in_circ=QtCore.QEasingCurve.OutInCirc,
    in_elastic=QtCore.QEasingCurve.InElastic,
    out_elastic=QtCore.QEasingCurve.OutElastic,
    in_out_elastic=QtCore.QEasingCurve.InOutElastic,
    out_in_elastic=QtCore.QEasingCurve.OutInElastic,
    in_back=QtCore.QEasingCurve.InBack,
    out_back=QtCore.QEasingCurve.OutBack,
    in_out_back=QtCore.QEasingCurve.InOutBack,
    out_in_back=QtCore.QEasingCurve.OutInBack,
    in_bounce=QtCore.QEasingCurve.InBounce,
    out_bounce=QtCore.QEasingCurve.OutBounce,
    in_out_bounce=QtCore.QEasingCurve.InOutBounce,
    out_in_bounce=QtCore.QEasingCurve.OutInBounce,
    bezier_spline=QtCore.QEasingCurve.BezierSpline,
    tcb_spline=QtCore.QEasingCurve.TCBSpline,
    custom=QtCore.QEasingCurve.Custom,
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
    def __init__(
        self, other_or_type: Union[TypeStr, int, QtCore.QEasingCurve] = "linear"
    ):
        if isinstance(other_or_type, str) and other_or_type in TYPE:
            other_or_type = TYPE[other_or_type]
        super().__init__(other_or_type)

    def __getitem__(self, value: float) -> float:
        return self.valueForProgress(value)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_type()!r})"

    def set_custom_type(self, method: CurveMethod):
        self.setCustomType(method)

    def get_custom_type(self) -> CurveMethod:
        return self.customType()

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
