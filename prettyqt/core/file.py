from __future__ import annotations

from prettyqt import core


class FileMixin(core.FileDeviceMixin):
    pass


class File(FileMixin, core.QFile):
    pass
