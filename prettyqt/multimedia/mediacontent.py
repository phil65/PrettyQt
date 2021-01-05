from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtMultimedia


class MediaContent(QtMultimedia.QMediaContent):
    def get_url(self):
        return core.Url(self.canonicalUrl())
