from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict, datatypes


mod = QtGui.QImageIOHandler

ImageOptionStr = Literal[
    "size",
    "clip_rect",
    "scaled_size",
    "scaled_clip_rect",
    "description",
    "compression_ratio",
    "gamma",
    "quality",
    "name",
    "subtype",
    "incremental_reading",
    "endianness",
    "animation",
    "background_color",
    # "image_format",
    "supported_sub_types",
    "optimized_write",
    "progressive_scan_write",
    "image_transformation",
]

IMAGE_OPTION: bidict[ImageOptionStr, mod.ImageOption] = bidict(
    size=mod.ImageOption.Size,
    clip_rect=mod.ImageOption.ClipRect,
    scaled_size=mod.ImageOption.ScaledSize,
    scaled_clip_rect=mod.ImageOption.ScaledClipRect,
    description=mod.ImageOption.Description,
    compression_ratio=mod.ImageOption.CompressionRatio,
    gamma=mod.ImageOption.Gamma,
    quality=mod.ImageOption.Quality,
    name=mod.ImageOption.Name,
    subtype=mod.ImageOption.SubType,
    incremental_reading=mod.ImageOption.IncrementalReading,
    endianness=mod.ImageOption.Endianness,
    animation=mod.ImageOption.Animation,
    background_color=mod.ImageOption.BackgroundColor,
    # image_format=mod.ImageOption.ImageFormat,
    supported_sub_types=mod.ImageOption.SupportedSubTypes,
    optimized_write=mod.ImageOption.OptimizedWrite,
    progressive_scan_write=mod.ImageOption.ProgressiveScanWrite,
    image_transformation=mod.ImageOption.ImageTransformation,
)

TransformationStr = Literal[
    "none",
    "mirror",
    "flip",
    "rotate_180",
    "roate_90",
    "mirror_and_rotate_90",
    "flip_and_rotate_90",
    "rotate_270",
]

TRANSFORMATION: bidict[TransformationStr, mod.Transformation] = bidict(
    none=mod.Transformation.TransformationNone,
    mirror=mod.Transformation.TransformationMirror,
    flip=mod.Transformation.TransformationFlip,
    rotate_180=mod.Transformation.TransformationRotate180,
    roate_90=mod.Transformation.TransformationRotate90,
    mirror_and_rotate_90=mod.Transformation.TransformationMirrorAndRotate90,
    flip_and_rotate_90=mod.Transformation.TransformationFlipAndRotate90,
    rotate_270=mod.Transformation.TransformationRotate270,
)


class ImageIOHandler(mod):
    """Defines the common image I/O interface for all image formats in Qt."""

    def __getitem__(self, key: ImageOptionStr | mod.ImageOption) -> datatypes.Variant:
        return self.get_option(key)

    def __setitem__(
        self, key: ImageOptionStr | mod.ImageOption, value: datatypes.Variant
    ):
        self.set_option(key, value)

    def get_format(self) -> str:
        return self.format().data().decode()

    def set_option(
        self, option: ImageOptionStr | mod.ImageOption, value: datatypes.Variant
    ):
        """Set option to given value.

        Args:
            option: option to use
            value: value to set
        """
        self.setOption(IMAGE_OPTION.get_enum_value(option), value)

    def get_option(self, option: ImageOptionStr | mod.ImageOption) -> datatypes.Variant:
        """Return the value assigned to option.

        Args:
            option: option to get

        Returns:
            option
        """
        return self.option(IMAGE_OPTION.get_enum_value(option))

    def supports_option(self, option: ImageOptionStr | mod.ImageOption) -> bool:
        """Return whether the image handler supports given option.

        Args:
            option: option to check

        Returns:
            option
        """
        return self.supportsOption(IMAGE_OPTION.get_enum_value(option))


if __name__ == "__main__":
    writer = ImageIOHandler()
