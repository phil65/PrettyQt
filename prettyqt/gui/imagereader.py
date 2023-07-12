from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.utils import bidict, datatypes


ImageReaderErrorStr = Literal[
    "file_not_found", "device", "unsupported_format", "invalid_data", "unknown"
]

IMAGE_READER_ERROR: bidict[ImageReaderErrorStr, gui.QImageReader.ImageReaderError] = (
    bidict(
        file_not_found=gui.QImageReader.ImageReaderError.FileNotFoundError,
        device=gui.QImageReader.ImageReaderError.DeviceError,
        unsupported_format=gui.QImageReader.ImageReaderError.UnsupportedFormatError,
        invalid_data=gui.QImageReader.ImageReaderError.InvalidDataError,
        unknown=gui.QImageReader.ImageReaderError.UnknownError,
    )
)


class ImageReader(gui.QImageReader):
    """Format independent interface for reading images from files or other devices."""

    def __getitem__(self, key: str) -> str:
        return self.text(key)

    def get_error(self) -> ImageReaderErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return IMAGE_READER_ERROR.inverse[self.error()]

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
        return self.format().data().decode()

    def get_subtype(self) -> str:
        return self.subType().data().decode()

    def get_supported_subtypes(self) -> list[str]:
        return [i.data().decode() for i in self.supportedSubTypes()]

    def set_format(self, fmt: datatypes.ByteArrayType):
        fmt = datatypes.to_bytearray(fmt)
        self.setFormat(fmt)

    def get_transformation(self) -> gui.imageiohandler.TransformationStr:
        """Return the transformation and orientation the image has been set to.

        Returns:
            transformation
        """
        return gui.imageiohandler.TRANSFORMATION.inverse[self.transformation()]

    def read_image(self) -> gui.Image:
        return gui.Image(self.read())

    def supports_option(
        self, option: gui.imageiohandler.ImageOptionStr | gui.QImageIOHandler.ImageOption
    ) -> bool:
        """Return whether the image handler supports given option.

        Args:
            option: option to check

        Returns:
            option
        """
        return self.supportsOption(gui.imageiohandler.IMAGE_OPTION.get_enum_value(option))

    @staticmethod
    def get_image_format(obj: str | core.QIODevice) -> str:
        return ImageReader.imageFormat(obj).data().decode()

    @staticmethod
    def get_supported_image_formats() -> list[str]:
        return [i.data().decode() for i in ImageReader.supportedImageFormats()]

    @staticmethod
    def get_supported_mime_types() -> list[str]:
        return [i.data().decode() for i in ImageReader.supportedMimeTypes()]

    @staticmethod
    def get_image_formats_for_mime_type(typ: datatypes.ByteArrayType) -> list[str]:
        typ = datatypes.to_bytearray(typ)
        return [i.data().decode() for i in ImageReader.imageFormatsForMimeType(typ)]


if __name__ == "__main__":
    writer = ImageReader()
    writer.set_subtype("A8R8G8B8")
