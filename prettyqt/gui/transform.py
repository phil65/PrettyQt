from __future__ import annotations

from typing import Literal, Self

from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr, serializemixin


TRANSFORMATION_TYPE = bidict(
    none=QtGui.QTransform.TransformationType.TxNone,
    translate=QtGui.QTransform.TransformationType.TxTranslate,
    scale=QtGui.QTransform.TransformationType.TxScale,
    rotate=QtGui.QTransform.TransformationType.TxRotate,
    shear=QtGui.QTransform.TransformationType.TxShear,
    project=QtGui.QTransform.TransformationType.TxProject,
)

TransformationTypeStr = Literal[
    "none", "translate", "scale", "rotate", "shear", "project"
]


class Transform(serializemixin.SerializeMixin, QtGui.QTransform):
    def __repr__(self):
        return get_repr(
            self,
            self.m11(),
            self.m12(),
            self.m13(),
            self.m21(),
            self.m22(),
            self.m23(),
            self.m31(),
            self.m32(),
            self.m33(),
        )

    def __getitem__(self, value: tuple[int, int]) -> float:  # noqa: PLR0911
        match value[0], value[1]:
            case 0, 0:
                return self.m11()
            case 0, 1:
                return self.m12()
            case 0, 2:
                return self.m13()
            case 1, 0:
                return self.m21()
            case 1, 1:
                return self.m22()
            case 1, 2:
                return self.m23()
            case 2, 0:
                return self.m31()
            case 2, 1:
                return self.m32()
            case 2, 2:
                return self.m33()
            case _:
                msg = f"Wrong value {value}"
                raise ValueError(msg)

    @property
    def _m11(self) -> float:
        return self.m11()

    @property
    def _m12(self) -> float:
        return self.m12()

    @property
    def _m13(self) -> float:
        return self.m13()

    @property
    def _m21(self) -> float:
        return self.m21()

    @property
    def _m22(self) -> float:
        return self.m22()

    @property
    def _m23(self) -> float:
        return self.m23()

    @property
    def _m31(self) -> float:
        return self.m31()

    @property
    def _m32(self) -> float:
        return self.m32()

    @property
    def _m33(self) -> float:
        return self.m33()

    __match_args__ = (
        "_m11",
        "_m12",
        "_m13",
        "_m21",
        "_m22",
        "_m23",
        "_m31",
        "_m32",
        "_m33",
    )

    @classmethod
    def clone_from(cls, transform: QtGui.QTransform) -> Self:
        return cls(
            transform.m11(),
            transform.m12(),
            transform.m13(),
            transform.m21(),
            transform.m22(),
            transform.m23(),
            transform.m31(),
            transform.m32(),
            transform.m33(),
        )

    def get_type(self) -> TransformationTypeStr:
        return TRANSFORMATION_TYPE.inverse[self.type()]


if __name__ == "__main__":
    transform = Transform()
