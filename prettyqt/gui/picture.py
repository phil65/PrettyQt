from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui
from prettyqt.utils import serializemixin


class Picture(serializemixin.SerializeMixin, gui.PaintDeviceMixin, QtGui.QPicture):
    pass
