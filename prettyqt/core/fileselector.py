import os

from prettyqt import core
from prettyqt.utils import datatypes


class FileSelector(core.ObjectMixin, core.QFileSelector):
    """Convenient way of selecting file variants."""

    def select_path(self, path: datatypes.PathType) -> str:
        return self.select(os.fspath(path))

    def select_url(self, url: datatypes.UrlType) -> core.Url:
        return core.Url(self.select(datatypes.to_url(url)))
