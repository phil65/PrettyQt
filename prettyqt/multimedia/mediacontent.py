from qtpy import QtMultimedia

from prettyqt import core


class MediaContent(QtMultimedia.QMediaContent):
    def get_url(self):
        return core.Url(self.canonicalUrl())
