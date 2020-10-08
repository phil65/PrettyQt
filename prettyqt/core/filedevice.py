# -*- coding: utf-8 -*-

from typing import Union, Optional
import datetime

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError, to_datetime

FILE_TIMES = bidict(
    access=QtCore.QFileDevice.FileAccessTime,
    birth=QtCore.QFileDevice.FileBirthTime,
    metadata_change=QtCore.QFileDevice.FileMetadataChangeTime,
    modification=QtCore.QFileDevice.FileModificationTime,
)

QtCore.QFileDevice.__bases__ = (core.IODevice,)


class FileDevice(QtCore.QFileDevice):
    def set_file_time(
        self, file_time: Union[QtCore.QDateTime, datetime.datetime], typ: str
    ) -> bool:
        """Set file time.

        Allowed values are "access", "birth", "metadata_change", "modification"

        Args:
            typ: file time to use

        Raises:
            InvalidParamError: file time does not exist
        """
        if typ not in FILE_TIMES:
            raise InvalidParamError(typ, FILE_TIMES)
        return self.setFileTime(file_time, FILE_TIMES[typ])

    def get_file_time(self, typ: str) -> Optional[datetime.datetime]:
        """Return current file time.

        Possible values: "access", "birth", "metadata_change", "modification"

        Returns:
            file time
        """
        if typ not in FILE_TIMES:
            raise InvalidParamError(typ, FILE_TIMES)
        date = self.fileTime(FILE_TIMES[typ])
        if not date:
            return None
        return to_datetime(date)
