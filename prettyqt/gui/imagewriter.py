from typing import List, Literal, Union

from qtpy import QtCore, QtGui

from prettyqt import gui
from prettyqt.utils import InvalidParamError, bidict


IMAGE_WRITER_ERROR = bidict(
    device=QtGui.QImageWriter.DeviceError,
    unsupported_format=QtGui.QImageWriter.UnsupportedFormatError,
    invalid_image=QtGui.QImageWriter.InvalidImageError,
    unknown=QtGui.QImageWriter.UnknownError,
)

ImageWriterErrorStr = Literal["device", "unsupported_format", "invalid_image", "unknown"]


class ImageWriter(QtGui.QImageWriter):
    def __setitem__(self, key: str, val: str):
        self.setText(key, val)

    def get_error(self) -> ImageWriterErrorStr:
        """Return error type.

        Returns:
            error type
        """
        return IMAGE_WRITER_ERROR.inverse[self.error()]

    def get_format(self) -> str:
        return bytes(self.format()).decode()

    def get_subtype(self) -> str:
        return bytes(self.subType()).decode()

    def get_supported_image_formats(self) -> List[str]:
        return [bytes(i).decode() for i in self.supportedImageFormats()]

    def get_supported_subtypes(self) -> List[str]:
        return [bytes(i).decode() for i in self.supportedSubTypes()]

    def set_subtype(self, subtype: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(subtype, str):
            subtype = subtype.encode()
        self.setSubType(subtype)

    def set_format(self, fmt: Union[str, bytes, QtCore.QByteArray]):
        if isinstance(fmt, str):
            fmt = fmt.encode()
        self.setFormat(fmt)

    def set_transformation(self, origin: gui.imageiohandler.TransformationStr):
        """Set the image transformations metadata including orientation.

        Args:
            origin: transformation to use

        Raises:
            InvalidParamError: transformation does not exist
        """
        if origin not in gui.imageiohandler.TRANSFORMATION:
            raise InvalidParamError(origin, gui.imageiohandler.TRANSFORMATION)
        self.setTransformation(gui.imageiohandler.TRANSFORMATION[origin])

    def get_transformation(self) -> gui.imageiohandler.TransformationStr:
        """Return the transformation and orientation the image has been set to.

        Returns:
            transformation
        """
        return gui.imageiohandler.TRANSFORMATION.inverse[self.transformation()]


if __name__ == "__main__":
    writer = ImageWriter()
    print(writer.get_supported_image_formats())
    print(writer.get_subtype())
    print(writer.get_format())
    writer.set_subtype("A8R8G8B8")
