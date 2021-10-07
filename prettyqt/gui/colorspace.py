from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


NAMED_COLOR_SPACE = bidict(
    srgb=QtGui.QColorSpace.NamedColorSpace.SRgb,
    srgb_linear=QtGui.QColorSpace.NamedColorSpace.SRgbLinear,
    adobe_rgb=QtGui.QColorSpace.NamedColorSpace.AdobeRgb,
    display_p3=QtGui.QColorSpace.NamedColorSpace.DisplayP3,
    pro_photo_rgb=QtGui.QColorSpace.NamedColorSpace.ProPhotoRgb,
)

NamedColorSpaceStr = Literal[
    "srgb", "srgb_linear", "adobe_rgb", "display_p3", "pro_photo_rgb"
]

PRIMARIES = bidict(
    custom=QtGui.QColorSpace.Primaries.Custom,
    srgb=QtGui.QColorSpace.Primaries.SRgb,
    adobe_rgb=QtGui.QColorSpace.Primaries.AdobeRgb,
    dci_p3_d65=QtGui.QColorSpace.Primaries.DciP3D65,
    pro_photo_rgb=QtGui.QColorSpace.Primaries.ProPhotoRgb,
)

PrimariesStr = Literal["custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb"]

TRANSFER_FUNCTION = bidict(
    custom=QtGui.QColorSpace.TransferFunction.Custom,
    linear=QtGui.QColorSpace.TransferFunction.Linear,
    gamma=QtGui.QColorSpace.TransferFunction.Gamma,
    srgb=QtGui.QColorSpace.TransferFunction.SRgb,
    pro_photo_rgb=QtGui.QColorSpace.TransferFunction.ProPhotoRgb,
)

TransformFunctionStr = Literal["custom", "linear", "gamma", "srgb", "pro_photo_rgb"]


class ColorSpace(QtGui.QColorSpace):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        super().__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __bool__(self):
        return self.isValid()

    def set_primaries(self, primaries: PrimariesStr):
        """Set primaries.

        Args:
            primaries: primaries to use

        Raises:
            InvalidParamError: primaries do not exist
        """
        if primaries not in PRIMARIES:
            raise InvalidParamError(primaries, PRIMARIES)
        self.setPrimaries(PRIMARIES[primaries])

    def get_primaries(self) -> PrimariesStr:
        """Return current primaries.

        Returns:
            primaries
        """
        return PRIMARIES.inverse[self.primaries()]

    def set_transfer_function(self, fn: TransformFunctionStr, gamma: float = 0.0):
        """Set transfer function.

        Args:
            fn: transfer function to use

        Raises:
            InvalidParamError: transfer function do not exist
        """
        if fn not in TRANSFER_FUNCTION:
            raise InvalidParamError(fn, TRANSFER_FUNCTION)
        self.setTransferFunction(TRANSFER_FUNCTION[fn], gamma)

    def get_transfer_function(self) -> TransformFunctionStr:
        """Return current transfer function.

        Returns:
            transfer function
        """
        return TRANSFER_FUNCTION.inverse[self.transferFunction()]


if __name__ == "__main__":
    space = ColorSpace()
    print(space.iccProfile())
