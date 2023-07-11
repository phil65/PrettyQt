from __future__ import annotations

from prettyqt import core


class Buffer(core.IODeviceMixin, core.QBuffer):
    """QIODevice interface for a QByteArray."""
