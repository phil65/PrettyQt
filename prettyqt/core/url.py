# -*- coding: utf-8 -*-

from typing import Union, Optional

import pathlib

from qtpy import QtCore


class Url(QtCore.QUrl):
    def __init__(self, path: Union[QtCore.QUrl, str, pathlib.Path] = None):
        if path is None:
            super().__init__()
        else:
            super().__init__(str(path) if not isinstance(path, QtCore.QUrl) else path)
            if isinstance(path, pathlib.Path):
                self.setScheme("file")

    # def __str__(self):
    #     return self.absolutePath()

    def __repr__(self):
        return f"core.Url('{self.toString(self.PreferLocalFile)}')"

    def __str__(self):
        return self.toString(self.PreferLocalFile)

    def serialize_fields(self):
        return dict(path=self.toString())

    def serialize(self):
        return self.serialize_fields()

    def to_path(self) -> pathlib.Path:
        """Get pathlib object from the URL.

        Returns:
            Path
        """
        return pathlib.Path(str(self))

    def is_local_file(self) -> bool:
        return self.isLocalFile()

    @classmethod
    def from_user_input(cls, url: str, working_dir: Optional[str] = None):
        if working_dir is None:
            working_dir = ""
        return cls(cls.fromUserInput(url, working_dir))
