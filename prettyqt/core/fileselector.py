from __future__ import annotations

import os
from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class FileSelector(core.ObjectMixin, QtCore.QFileSelector):
    def serialize_fields(self):
        return dict(extra_selectors=self.extraSelectors())

    def select_path(self, path: datatypes.PathType) -> str:
        return self.select(os.fspath(path))

    def select_url(self, url: datatypes.UrlType) -> core.Url:
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        return core.Url(self.select(url))
