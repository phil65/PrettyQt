from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict, serializemixin


NamedColorSpaceStr = Literal[
    "srgb",
    "srgb_linear",
    "adobe_rgb",
    "display_p3",
    "pro_photo_rgb",
    "bt2020",
    "bt2100_pq",
    "bt2100_hlg",
]

NAMED_COLOR_SPACE: bidict[NamedColorSpaceStr, QtGui.QColorSpace.NamedColorSpace] = bidict(
    srgb=QtGui.QColorSpace.NamedColorSpace.SRgb,
    srgb_linear=QtGui.QColorSpace.NamedColorSpace.SRgbLinear,
    adobe_rgb=QtGui.QColorSpace.NamedColorSpace.AdobeRgb,
    display_p3=QtGui.QColorSpace.NamedColorSpace.DisplayP3,
    pro_photo_rgb=QtGui.QColorSpace.NamedColorSpace.ProPhotoRgb,
    bt2020=QtGui.QColorSpace.NamedColorSpace.Bt2020,
    bt2100_pq=QtGui.QColorSpace.NamedColorSpace.Bt2100Pq,
    bt2100_hlg=QtGui.QColorSpace.NamedColorSpace.Bt2100Hlg,
)

PrimariesStr = Literal[
    "custom", "srgb", "adobe_rgb", "dci_p3_d65", "pro_photo_rgb", "bt2020"
]

PRIMARIES: bidict[PrimariesStr, QtGui.QColorSpace.Primaries] = bidict(
    custom=QtGui.QColorSpace.Primaries.Custom,
    srgb=QtGui.QColorSpace.Primaries.SRgb,
    adobe_rgb=QtGui.QColorSpace.Primaries.AdobeRgb,
    dci_p3_d65=QtGui.QColorSpace.Primaries.DciP3D65,
    pro_photo_rgb=QtGui.QColorSpace.Primaries.ProPhotoRgb,
    bt2020=QtGui.QColorSpace.Primaries.Bt2020,
)


TransformFunctionStr = Literal[
    "custom", "linear", "gamma", "srgb", "pro_photo_rgb", "bt2020", "st2084", "hlg"
]

TRANSFER_FUNCTION: bidict[TransformFunctionStr, QtGui.QColorSpace.TransferFunction] = (
    bidict(
        custom=QtGui.QColorSpace.TransferFunction.Custom,
        linear=QtGui.QColorSpace.TransferFunction.Linear,
        gamma=QtGui.QColorSpace.TransferFunction.Gamma,
        srgb=QtGui.QColorSpace.TransferFunction.SRgb,
        pro_photo_rgb=QtGui.QColorSpace.TransferFunction.ProPhotoRgb,
        bt2020=QtGui.QColorSpace.TransferFunction.Bt2020,
        st2084=QtGui.QColorSpace.TransferFunction.St2084,
        hlg=QtGui.QColorSpace.TransferFunction.Hlg,
    )
)

ColorModelStr = Literal["undefined", "rgb", "gray", "cmyk"]

COLOR_MODEL: bidict[ColorModelStr, QtGui.QColorSpace.ColorModel] = bidict(
    undefined=QtGui.QColorSpace.ColorModel.Undefined,
    rgb=QtGui.QColorSpace.ColorModel.Rgb,
    gray=QtGui.QColorSpace.ColorModel.Gray,
    cmyk=QtGui.QColorSpace.ColorModel.Cmyk,
)

TransformModelStr = Literal["three_component_matrix", "element_list_processing"]

TRANSFORM_MODEL: bidict[TransformModelStr, QtGui.QColorSpace.TransformModel] = bidict(
    three_component_matrix=QtGui.QColorSpace.TransformModel.ThreeComponentMatrix,
    element_list_processing=QtGui.QColorSpace.TransformModel.ElementListProcessing,
)


class ColorSpace(serializemixin.SerializeMixin, QtGui.QColorSpace):
    """Color space abstraction."""

    def __bool__(self):
        return self.isValid()

    def set_primaries(self, primaries: PrimariesStr | QtGui.QColorSpace.Primaries):
        """Set primaries.

        Args:
            primaries: primaries to use
        """
        self.setPrimaries(PRIMARIES.get_enum_value(primaries))

    def get_primaries(self) -> PrimariesStr:
        """Return current primaries.

        Returns:
            primaries
        """
        return PRIMARIES.inverse[self.primaries()]

    def set_transfer_function(
        self,
        fn: TransformFunctionStr | QtGui.QColorSpace.TransferFunction,
        gamma: float = 0.0,
    ):
        """Set transfer function.

        Args:
            fn: transfer function to use
            gamma: gamma value
        """
        self.setTransferFunction(TRANSFER_FUNCTION.get_enum_value(fn), gamma)

    def get_transfer_function(self) -> TransformFunctionStr:
        """Return current transfer function.

        Returns:
            transfer function
        """
        return TRANSFER_FUNCTION.inverse[self.transferFunction()]


if __name__ == "__main__":
    space = ColorSpace()
