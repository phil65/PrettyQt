from typing import List, Union

from qtpy import QtGui, QtCore

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError


IMAGE_WRITER_ERROR = bidict(
    device=QtGui.QImageWriter.DeviceError,
    unsupported_format=QtGui.QImageWriter.UnsupportedFormatError,
    invalid_image=QtGui.QImageWriter.InvalidImageError,
    unknown=QtGui.QImageWriter.UnknownError,
)

TRANSFORMATIONS = gui.imageiohandler.TRANSFORMATIONS


class ImageWriter(QtGui.QImageWriter):
    def __setitem__(self, key: str, val: str):
        self.setText(key, val)

    def get_error(self) -> str:
        """Return error type.

        possible values are "device", "unsupported_format", "invalid_image", "unknown"

        Returns:
            error type
        """
        return IMAGE_WRITER_ERROR.inv[self.error()]

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

    def set_transformation(self, origin: str):
        """Set the image transformations metadata including orientation.

        Allowed values are "none", "mirror", "flip", "rotate_180", "roate_90",
                           "mirror_and_rotate_90", "flip_and_rotate_90", "rotate_270"

        Args:
            origin: transformation to use

        Raises:
            InvalidParamError: transformation does not exist
        """
        if origin not in TRANSFORMATIONS:
            raise InvalidParamError(origin, TRANSFORMATIONS)
        self.setTransformation(TRANSFORMATIONS[origin])

    def get_transformation(self) -> str:
        """Return the transformation and orientation the image has been set to.

        Possible values: "none", "mirror", "flip", "rotate_180", "roate_90",
                         "mirror_and_rotate_90", "flip_and_rotate_90", "rotate_270"

        Returns:
            transformation
        """
        return TRANSFORMATIONS.inv[self.transformation()]


if __name__ == "__main__":
    writer = ImageWriter()
    print(writer.get_supported_image_formats())
    print(writer.get_subtype())
    print(writer.get_format())
    writer.set_subtype("A8R8G8B8")
