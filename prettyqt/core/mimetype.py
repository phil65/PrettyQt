from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class MimeType(QtCore.QMimeType):
    """Describes types of file or data, represented by a MIME type string."""

    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.name())

    def __str__(self):
        return self.name()
