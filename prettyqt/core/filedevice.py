import datetime
from typing import Literal, Optional, Union

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict, to_datetime


FILE_ERROR = bidict(
    none=QtCore.QFileDevice.NoError,
    read=QtCore.QFileDevice.ReadError,
    write=QtCore.QFileDevice.WriteError,
    fatal=QtCore.QFileDevice.FatalError,
    resource=QtCore.QFileDevice.ResourceError,
    open=QtCore.QFileDevice.OpenError,
    abort=QtCore.QFileDevice.AbortError,
    time_out=QtCore.QFileDevice.TimeOutError,
    unspecified=QtCore.QFileDevice.UnspecifiedError,
    remove=QtCore.QFileDevice.RemoveError,
    rename=QtCore.QFileDevice.RenameError,
    position=QtCore.QFileDevice.PositionError,
    resize=QtCore.QFileDevice.ResizeError,
    permissions=QtCore.QFileDevice.PermissionsError,
    copy=QtCore.QFileDevice.CopyError,
)

FileErrorStr = Literal[
    "none",
    "read",
    "write",
    "fatal",
    "resource",
    "open",
    "abort",
    "time_out",
    "unspecified",
    "remove",
    "rename",
    "position",
    "resize",
    "permissions",
    "copy",
]

FILE_TIME = bidict(
    access=QtCore.QFileDevice.FileAccessTime,
    birth=QtCore.QFileDevice.FileBirthTime,
    metadata_change=QtCore.QFileDevice.FileMetadataChangeTime,
    modification=QtCore.QFileDevice.FileModificationTime,
)

FileTimeStr = Literal["access", "birth", "metadata_change", "modification"]

PERMISSIONS = bidict(
    read_owner=QtCore.QFileDevice.ReadOwner,
    write_owner=QtCore.QFileDevice.WriteOwner,
    exe_owner=QtCore.QFileDevice.ExeOwner,
    read_user=QtCore.QFileDevice.ReadUser,
    write_user=QtCore.QFileDevice.WriteUser,
    exe_user=QtCore.QFileDevice.ExeUser,
    read_group=QtCore.QFileDevice.ReadGroup,
    write_group=QtCore.QFileDevice.WriteGroup,
    exe_group=QtCore.QFileDevice.ExeGroup,
    read_other=QtCore.QFileDevice.ReadOther,
    write_other=QtCore.QFileDevice.WriteOther,
    exe_other=QtCore.QFileDevice.ExeOther,
)

QtCore.QFileDevice.__bases__ = (core.IODevice,)


class FileDevice(QtCore.QFileDevice):
    def __repr__(self):
        return f"{type(self).__name__}({self.fileName()!r})"

    def __str__(self):
        return self.fileName()

    def set_file_time(
        self, file_time: Union[QtCore.QDateTime, datetime.datetime], typ: FileTimeStr
    ) -> bool:
        """Set file time.

        Args:
            typ: file time to use

        Raises:
            InvalidParamError: file time does not exist
        """
        if typ not in FILE_TIME:
            raise InvalidParamError(typ, FILE_TIME)
        return self.setFileTime(file_time, FILE_TIME[typ])

    def get_file_time(self, typ: FileTimeStr) -> Optional[datetime.datetime]:
        """Return current file time.

        Returns:
            file time
        """
        if typ not in FILE_TIME:
            raise InvalidParamError(typ, FILE_TIME)
        date = self.fileTime(FILE_TIME[typ])
        if not date:
            return None
        return to_datetime(date)

    def get_error(self) -> FileErrorStr:
        """Return file error status.

        Returns:
            file error status
        """
        return FILE_ERROR.inverse[self.error()]
