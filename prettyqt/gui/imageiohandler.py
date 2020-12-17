from typing import Any, Literal

from qtpy import QtGui

from prettyqt.utils import InvalidParamError, bidict, mappers


IMAGE_OPTION = bidict(
    size=QtGui.QImageIOHandler.Size,
    clip_rect=QtGui.QImageIOHandler.ClipRect,
    scaled_size=QtGui.QImageIOHandler.ScaledSize,
    scaled_clip_rect=QtGui.QImageIOHandler.ScaledClipRect,
    description=QtGui.QImageIOHandler.Description,
    compression_ratio=QtGui.QImageIOHandler.CompressionRatio,
    gamma=QtGui.QImageIOHandler.Gamma,
    quality=QtGui.QImageIOHandler.Quality,
    name=QtGui.QImageIOHandler.Name,
    subtype=QtGui.QImageIOHandler.SubType,
    incremental_reading=QtGui.QImageIOHandler.IncrementalReading,
    endianness=QtGui.QImageIOHandler.Endianness,
    animation=QtGui.QImageIOHandler.Animation,
    background_color=QtGui.QImageIOHandler.BackgroundColor,
    # image_format=QtGui.QImageIOHandler.ImageFormat,
    supported_sub_types=QtGui.QImageIOHandler.SupportedSubTypes,
    optimized_write=QtGui.QImageIOHandler.OptimizedWrite,
    progressive_scan_write=QtGui.QImageIOHandler.ProgressiveScanWrite,
    image_transformation=QtGui.QImageIOHandler.ImageTransformation,
    transformation_by_default=QtGui.QImageIOHandler.TransformedByDefault,
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
    "transformation_by_default",
]

TRANSFORMATION = mappers.FlagMap(
    QtGui.QImageIOHandler.Transformations,
    none=QtGui.QImageIOHandler.TransformationNone,
    mirror=QtGui.QImageIOHandler.TransformationMirror,
    flip=QtGui.QImageIOHandler.TransformationFlip,
    rotate_180=QtGui.QImageIOHandler.TransformationRotate180,
    roate_90=QtGui.QImageIOHandler.TransformationRotate90,
    mirror_and_rotate_90=QtGui.QImageIOHandler.TransformationMirrorAndRotate90,
    flip_and_rotate_90=QtGui.QImageIOHandler.TransformationFlipAndRotate90,
    rotate_270=QtGui.QImageIOHandler.TransformationRotate270,
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


class ImageIOHandler(QtGui.QImageIOHandler):
    def __getitem__(self, key: ImageOptionStr):
        return self.get_option(key)

    def __setitem__(self, key: ImageOptionStr, value):
        self.set_option(key, value)

    def get_format(self) -> str:
        return bytes(self.format()).decode()

    def set_option(self, option: ImageOptionStr, value):
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

    def get_option(self, option: ImageOptionStr) -> Any:
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
