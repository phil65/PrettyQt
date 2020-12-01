from typing import List, Union

from qtpy import QtGui, QtCore

from prettyqt import gui, core
from prettyqt.utils import bidict, InvalidParamError


IMAGE_READER_ERROR = bidict(
    file_not_found=QtGui.QImageReader.FileNotFoundError,
    device=QtGui.QImageReader.DeviceError,
    unsupported_format=QtGui.QImageReader.UnsupportedFormatError,
    invalid_data=QtGui.QImageReader.InvalidDataError,
    unknown=QtGui.QImageReader.UnknownError,
)

TRANSFORMATIONS = gui.imageiohandler.TRANSFORMATIONS
IMAGE_OPTION = gui.imageiohandler.IMAGE_OPTION


class ImageReader(QtGui.QImageReader):
    def __getitem__(self, key: str) -> str:
        return self.text(key)

    def get_error(self) -> str:
        """Return error type.

        possible values are "file_not_found", "device", "unsupported_format",
                            "invalid_image", "unknown"

        Returns:
            error type
        """
        return IMAGE_READER_ERROR.inv[self.error()]

    def get_background_color(self) -> gui.Color:
        return gui.Color(self.backgroundColor())

    def get_clip_rect(self) -> core.Rect:
        return core.Rect(self.clipRect())

    def get_current_image_rect(self) -> core.Rect:
        return core.Rect(self.currentImageRect())

    def get_scaled_clip_rect(self) -> core.Rect:
        return core.Rect(self.scaledClipRect())

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_scaled_size(self) -> core.Size:
        return core.Size(self.scaledSize())

    def get_format(self) -> str:
        return bytes(self.format()).decode()

    def get_subtype(self) -> str:
        return bytes(self.subType()).decode()

    def get_supported_subtypes(self) -> List[str]:
        return [bytes(i).decode() for i in self.supportedSubTypes()]

    def set_format(self, fmt: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(fmt, str):
            fmt = fmt.encode()
        self.setFormat(fmt)

    def get_transformation(self) -> str:
        """Return the transformation and orientation the image has been set to.

        Possible values: "none", "mirror", "flip", "rotate_180", "roate_90",
                         "mirror_and_rotate_90", "flip_and_rotate_90", "rotate_270"

        Returns:
            transformation
        """
        return TRANSFORMATIONS.inv[self.transformation()]

    def read_image(self) -> gui.Image:
        return gui.Image(self.read())

    def supports_option(self, option: str) -> bool:
        """Return whether the image handler supports given option.

        Possible values: "size", "clip_rect", "scaled_size", "scaled_clip_rect",
                         "description", "compression_ratio", "gamma", "quallity",
                         "name", "subtype", "incremental_reading", "endianness",
                         "animation", "background_color", "image_format",
                         "supported_sub_types", "optimized_write",
                         "progressive_scan_write", "image_transformation",
                         "transformation_by_default"

        Args:
            origin: option to check

        Returns:
            option
        """
        if option not in IMAGE_OPTION:
            raise InvalidParamError(option, IMAGE_OPTION)
        return self.supportsOption(IMAGE_OPTION[option])

    @staticmethod
    def get_image_format(obj: Union[str, QtCore.QIODevice]) -> str:
        return bytes(ImageReader.imageFormat(obj)).decode()

    @staticmethod
    def get_supported_image_formats() -> List[str]:
        return [bytes(i).decode() for i in ImageReader.supportedImageFormats()]

    @staticmethod
    def get_supported_mime_types() -> List[str]:
        return [bytes(i).decode() for i in ImageReader.supportedMimeTypes()]

    @staticmethod
    def get_image_formats_for_mime_type(
        typ: Union[str, bytes, QtCore.QByteArray]
    ) -> List[str]:
        if isinstance(typ, str):
            typ = typ.encode()
        return [bytes(i).decode() for i in ImageReader.imageFormatsForMimeType(typ)]


if __name__ == "__main__":
    writer = ImageReader()
    print(writer.get_supported_image_formats())
    print(writer.get_subtype())
    print(writer.get_format())
    writer.set_subtype("A8R8G8B8")
