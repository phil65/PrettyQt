from __future__ import annotations

from prettyqt import core


class SaveFile(core.FileDeviceMixin, core.QSaveFile):
    """Interface for safely writing to files."""
