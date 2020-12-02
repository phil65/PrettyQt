# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


NAMED_COLOR_SPACE = bidict(
    srgb=QtGui.QColorSpace.SRgb,
    srgb_linear=QtGui.QColorSpace.SRgbLinear,
    adobe_rgb=QtGui.QColorSpace.AdobeRgb,
    display_p3=QtGui.QColorSpace.DisplayP3,
    pro_photo_rgb=QtGui.QColorSpace.ProPhotoRgb,
)

PRIMARIES = bidict(
    custom=QtGui.QColorSpace.Primaries.Custom,
    srgb=QtGui.QColorSpace.Primaries.SRgb,
    adobe_rgb=QtGui.QColorSpace.Primaries.AdobeRgb,
    dci_p3_d65=QtGui.QColorSpace.Primaries.DciP3D65,
    pro_photo_rgb=QtGui.QColorSpace.Primaries.ProPhotoRgb,
)

TRANSFER_FUNCTION = bidict(
    custom=QtGui.QColorSpace.TransferFunction.Custom,
    linear=QtGui.QColorSpace.TransferFunction.Linear,
    gamma=QtGui.QColorSpace.TransferFunction.Gamma,
    srgb=QtGui.QColorSpace.TransferFunction.SRgb,
    pro_photo_rgb=QtGui.QColorSpace.TransferFunction.ProPhotoRgb,
)


class ColorSpace(QtGui.QColorSpace):
    def __getstate__(self):
        return core.DataStream.create_bytearray(self)

    def __setstate__(self, ba):
        super().__init__()
        core.DataStream.write_bytearray(ba, self)

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __bool__(self):
        return self.isValid()

    def set_primaries(self, primaries: str):
        """Set primaries.

        Allowed values are "custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb"

        Args:
            primaries: primaries to use

        Raises:
            InvalidParamError: primaries do not exist
        """
        if primaries not in PRIMARIES:
            raise InvalidParamError(primaries, PRIMARIES)
        self.setPrimaries(PRIMARIES[primaries])

    def get_primaries(self) -> str:
        """Return current primaries.

        Possible values: "custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb"

        Returns:
            primaries
        """
        return PRIMARIES.inv[self.primaries()]

    def set_transfer_function(self, fn: str, gamma: float = 0.0):
        """Set transfer function.

        Allowed values are "custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb"

        Args:
            fn: transfer function to use

        Raises:
            InvalidParamError: transfer function do not exist
        """
        if fn not in TRANSFER_FUNCTION:
            raise InvalidParamError(fn, TRANSFER_FUNCTION)
        self.setTransferFunction(TRANSFER_FUNCTION[fn], gamma)

    def get_transfer_function(self) -> str:
        """Return current transfer function.

        Possible values: "custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb"

        Returns:
            transfer function
        """
        return TRANSFER_FUNCTION.inv[self.transferFunction()]


if __name__ == "__main__":
    space = ColorSpace()
    print(space.iccProfile())
