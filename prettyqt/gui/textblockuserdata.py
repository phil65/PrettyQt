from __future__ import annotations

from prettyqt.qt import QtGui


class TextBlockUserData(QtGui.QTextBlockUserData):
    """Storage for the user data associated with each line."""

    def __init__(self, **kwds):
        for key, value in kwds.items():
            setattr(self, key, value)
        super().__init__()

    def __repr__(self):
        attrs = [i for i in dir(self) if not i.startswith("__")]
        kwds = ", ".join(f"{attr}={getattr(self, attr)!r}" for attr in attrs)
        return f"{type(self).__name__}({kwds})"
