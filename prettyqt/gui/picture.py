from __future__ import annotations

from prettyqt import gui
from prettyqt.utils import serializemixin


class Picture(serializemixin.SerializeMixin, gui.PaintDeviceMixin, gui.QPicture):
    """Paint device that records and replays QPainter commands."""
