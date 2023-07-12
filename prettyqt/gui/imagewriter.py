from __future__ import annotations

from typing import Literal

from prettyqt import gui
from prettyqt.utils import bidict, datatypes


ImageWriterErrorStr = Literal["device", "unsupported_format", "invalid_image", "unknown"]

IMAGE_WRITER_ERROR: bidict[ImageWriterErrorStr, gui.QImageWriter.ImageWriterError] = (
    bidict(
        device=gui.QImageWriter.ImageWriterError.DeviceError,
        unsupported_format=gui.QImageWriter.ImageWriterError.UnsupportedFormatError,
        invalid_image=gui.QImageWriter.ImageWriterError.InvalidImageError,
        unknown=gui.QImageWriter.ImageWriterError.UnknownError,
    )
)


class ImageWriter(gui.QImageWriter):
    """Format independent interface for writing images to files or other devices."""

    def __setitem__(self, key: str, val: str):
        self.setText(key, val)

    def get_error(self) -> ImageWriterErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return IMAGE_WRITER_ERROR.inverse[self.error()]

    def get_format(self) -> str:
        return self.format().data().decode()

    def get_subtype(self) -> str:
        return self.subType().data().decode()

    def get_supported_image_formats(self) -> list[str]:
        return [i.data().decode() for i in self.supportedImageFormats()]

    def get_supported_subtypes(self) -> list[str]:
        return [i.data().decode() for i in self.supportedSubTypes()]

    def set_subtype(self, subtype: datatypes.ByteArrayType):
        subtype = datatypes.to_bytearray(subtype)
        self.setSubType(subtype)

    def set_format(self, fmt: datatypes.ByteArrayType):
        fmt = datatypes.to_bytearray(fmt)
        self.setFormat(fmt)

    def set_transformation(
        self,
        origin: gui.imageiohandler.TransformationStr | gui.ImageIOHandler.Transformation,
    ):
        """Set the image transformations metadata including orientation.

        Args:
            origin: transformation to use
        """
        self.setTransformation(gui.imageiohandler.TRANSFORMATION.get_enum_value(origin))

    def get_transformation(self) -> gui.imageiohandler.TransformationStr:
        """Return the transformation and orientation the image has been set to.

        Returns:
            transformation
        """
        return gui.imageiohandler.TRANSFORMATION.inverse[self.transformation()]


if __name__ == "__main__":
    writer = ImageWriter()
    writer.set_subtype("A8R8G8B8")
