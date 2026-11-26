from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from prettyqt.qt import QtCore

    _FileBase = QtCore.QFile
else:
    _FileBase = object


class FileMixin(core.FileDeviceMixin, _FileBase):
    pass


class File(FileMixin, core.QFile):
    """Interface for reading from and writing to files."""
