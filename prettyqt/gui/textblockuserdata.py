from __future__ import annotations

from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class TextBlockUserData(QtGui.QTextBlockUserData):
    """Storage for the user data associated with each line."""

    def __init__(self, **kwds):
        for key, value in kwds.items():
            setattr(self, key, value)
        super().__init__()

    def __repr__(self):
        kwargs = {i: getattr(self, i) for i in dir(self) if not i.startswith("__")}
        return get_repr(self, **kwargs)
