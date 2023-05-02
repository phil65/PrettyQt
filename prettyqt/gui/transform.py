from __future__ import annotations

from typing import Literal

from typing_extensions import Self

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

    def __getitem__(self, value: tuple[int, int]) -> float:
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
        raise ValueError(f"Wrong value {value}")

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
    print(transform[0, 0])
    print(repr(transform))
