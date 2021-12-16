from __future__ import annotations

import os

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import types


QtCore.QFileSelector.__bases__ = (core.Object,)


class FileSelector(QtCore.QFileSelector):
    def serialize_fields(self):
        return dict(extra_selectors=self.extraSelectors())

    def select_path(self, path: types.PathType) -> str:
        return self.select(os.fspath(path))

    def select_url(self, url: types.UrlType) -> core.Url:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        return core.Url(self.select(url))
