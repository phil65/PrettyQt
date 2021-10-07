from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict, mappers, types


mod = QtGui.QImageIOHandler

IMAGE_OPTION = bidict(
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

TRANSFORMATION = mappers.FlagMap(
    mod.Transformation,
    none=mod.Transformation.TransformationNone,
    mirror=mod.Transformation.TransformationMirror,
    flip=mod.Transformation.TransformationFlip,
    rotate_180=mod.Transformation.TransformationRotate180,
    roate_90=mod.Transformation.TransformationRotate90,
    mirror_and_rotate_90=mod.Transformation.TransformationMirrorAndRotate90,
    flip_and_rotate_90=mod.Transformation.TransformationFlipAndRotate90,
    rotate_270=mod.Transformation.TransformationRotate270,
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


class ImageIOHandler(mod):
    def __getitem__(self, key: ImageOptionStr) -> types.Variant:
        return self.get_option(key)

    def __setitem__(self, key: ImageOptionStr, value: types.Variant):
        self.set_option(key, value)

    def get_format(self) -> str:
        return bytes(self.format()).decode()

    def set_option(self, option: ImageOptionStr, value: types.Variant):
        """Set option to given value.

        Args:
            option: option to use
            value: value to set

        Raises:
            InvalidParamError: option does not exist
        """
        if option not in IMAGE_OPTION:
            raise InvalidParamError(option, IMAGE_OPTION)
        self.setOption(IMAGE_OPTION[option], value)

    def get_option(self, option: ImageOptionStr) -> types.Variant:
        """Return the value assigned to option.

        Args:
            option: option to get

        Returns:
            option
        """
        if option not in IMAGE_OPTION:
            raise InvalidParamError(option, IMAGE_OPTION)
        return self.option(IMAGE_OPTION[option])

    def supports_option(self, option: ImageOptionStr) -> bool:
        """Return whether the image handler supports given option.

        Args:
            option: option to check

        Returns:
            option
        """
        if option not in IMAGE_OPTION:
            raise InvalidParamError(option, IMAGE_OPTION)
        return self.supportsOption(IMAGE_OPTION[option])


if __name__ == "__main__":
    writer = ImageIOHandler()
