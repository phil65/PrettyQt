from __future__ import annotations

import datetime

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict, datatypes, get_repr


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

FILE_ERROR: bidict[FileErrorStr, core.QFileDevice.FileError] = bidict(
    none=core.QFileDevice.FileError.NoError,
    read=core.QFileDevice.FileError.ReadError,
    write=core.QFileDevice.FileError.WriteError,
    fatal=core.QFileDevice.FileError.FatalError,
    resource=core.QFileDevice.FileError.ResourceError,
    open=core.QFileDevice.FileError.OpenError,
    abort=core.QFileDevice.FileError.AbortError,
    time_out=core.QFileDevice.FileError.TimeOutError,
    unspecified=core.QFileDevice.FileError.UnspecifiedError,
    remove=core.QFileDevice.FileError.RemoveError,
    rename=core.QFileDevice.FileError.RenameError,
    position=core.QFileDevice.FileError.PositionError,
    resize=core.QFileDevice.FileError.ResizeError,
    permissions=core.QFileDevice.FileError.PermissionsError,
    copy=core.QFileDevice.FileError.CopyError,
)

FileTimeStr = Literal["access", "birth", "metadata_change", "modification"]

FILE_TIME: bidict[FileTimeStr, core.QFileDevice.FileTime] = bidict(
    access=core.QFileDevice.FileTime.FileAccessTime,
    birth=core.QFileDevice.FileTime.FileBirthTime,
    metadata_change=core.QFileDevice.FileTime.FileMetadataChangeTime,
    modification=core.QFileDevice.FileTime.FileModificationTime,
)

PermissionStr = Literal[
    "read_owner",
    "write_owner",
    "exe_owner",
    "read_user",
    "write_user",
    "exe_user",
    "read_group",
    "write_group",
    "exe_group",
    "read_other",
    "write_other",
    "exe_other",
]

PERMISSIONS: bidict[PermissionStr, core.QFileDevice.Permission] = bidict(
    read_owner=core.QFileDevice.Permission.ReadOwner,
    write_owner=core.QFileDevice.Permission.WriteOwner,
    exe_owner=core.QFileDevice.Permission.ExeOwner,
    read_user=core.QFileDevice.Permission.ReadUser,
    write_user=core.QFileDevice.Permission.WriteUser,
    exe_user=core.QFileDevice.Permission.ExeUser,
    read_group=core.QFileDevice.Permission.ReadGroup,
    write_group=core.QFileDevice.Permission.WriteGroup,
    exe_group=core.QFileDevice.Permission.ExeGroup,
    read_other=core.QFileDevice.Permission.ReadOther,
    write_other=core.QFileDevice.Permission.WriteOther,
    exe_other=core.QFileDevice.Permission.ExeOther,
)


class FileDeviceMixin(core.IODeviceMixin):
    def __repr__(self):
        return get_repr(self, self.fileName())

    def __str__(self):
        return self.fileName()

    # def __fspath__(self) -> str:
    #     return self.fileName()

    def get_permissions(self) -> list[PermissionStr]:
        return PERMISSIONS.get_list(self.permissions())

    def set_file_time(
        self,
        file_time: datatypes.DateTimeType,
        typ: FileTimeStr | core.QFileDevice.FileTime,
    ) -> bool:
        """Set file time.

        Args:
            file_time: file time to set
            typ: file time type
        """
        file_time = datatypes.to_datetime(file_time)
        return self.setFileTime(file_time, FILE_TIME.get_enum_value(typ))  # type: ignore

    def get_file_time(
        self, typ: FileTimeStr | core.QFileDevice.FileTime
    ) -> datetime.datetime | None:
        """Return current file time.

        Returns:
            file time
        """
        if date := self.fileTime(FILE_TIME.get_enum_value(typ)):
            return date.toPython()  # type: ignore
        return None

    def get_error(self) -> FileErrorStr:
        """Return file error status.

        Returns:
            file error status
        """
        return FILE_ERROR.inverse[self.error()]

    def is_readable(self) -> bool:
        """Returns whether file has ReadUser permission flag."""
        return self.permissions() & core.QFileDevice.Permission.ReadUser

    def is_writable(self) -> bool:
        """Returns whether file has WriteUser permission flag."""
        return self.permissions() & core.QFileDevice.Permission.WriteUser

    def is_executable(self) -> bool:
        """Returns whether file has ExeUser permission flag."""
        return self.permissions() & core.QFileDevice.Permission.ExeUser


class FileDevice(FileDeviceMixin, core.QFileDevice):
    pass
