from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import bidict


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


class Transform(QtGui.QTransform):
    def __getstate__(self):
        return bytes(self)

    def __repr__(self):
        return (
            f"{type(self).__name__}({self.m11()}, {self.m12()}, {self.m13()}, "
            f"{self.m21()}, {self.m22()}, {self.m23()}, {self.m31()}, {self.m32()}, "
            f"{self.m33()})"
        )

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

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

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    @classmethod
    def clone_from(cls, transform: QtGui.QTransform) -> Transform:
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
