from typing import List, Literal, Union

from qtpy import QtCore, QtGui

from prettyqt import core, gui
from prettyqt.utils import InvalidParamError, bidict


IMAGE_READER_ERROR = bidict(
    file_not_found=QtGui.QImageReader.FileNotFoundError,
    device=QtGui.QImageReader.DeviceError,
    unsupported_format=QtGui.QImageReader.UnsupportedFormatError,
    invalid_data=QtGui.QImageReader.InvalidDataError,
    unknown=QtGui.QImageReader.UnknownError,
)

ImageReaderErrorStr = Literal[
    "file_not_found", "device", "unsupported_format", "invalid_data", "unknown"
]


class ImageReader(QtGui.QImageReader):
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
        return bytes(self.format()).decode()

    def get_subtype(self) -> str:
        return bytes(self.subType()).decode()

    def get_supported_subtypes(self) -> List[str]:
        return [bytes(i).decode() for i in self.supportedSubTypes()]

    def set_format(self, fmt: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(fmt, str):
            fmt = fmt.encode()
        self.setFormat(fmt)

    def get_transformation(self) -> gui.imageiohandler.TransformationStr:
        """Return the transformation and orientation the image has been set to.

        Returns:
            transformation
        """
        return gui.imageiohandler.TRANSFORMATION.inverse[self.transformation()]

    def read_image(self) -> gui.Image:
        return gui.Image(self.read())

    def supports_option(self, option: gui.imageiohandler.ImageOptionStr) -> bool:
        """Return whether the image handler supports given option.

        Args:
            option: option to check

        Returns:
            option
        """
        if option not in gui.imageiohandler.IMAGE_OPTION:
            raise InvalidParamError(option, gui.imageiohandler.IMAGE_OPTION)
        return self.supportsOption(gui.imageiohandler.IMAGE_OPTION[option])

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
