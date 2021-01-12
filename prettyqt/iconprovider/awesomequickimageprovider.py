from __future__ import annotations

from prettyqt import iconprovider, quick
from prettyqt.qt import QtCore


class AwesomeQuickImageProvider(quick.QuickImageProvider):
    def requestPixmap(self, id_: str, requested_size: QtCore.QSize):  # type: ignore
        pix = iconprovider.get_icon(id_).pixmap(requested_size)
        return pix, pix.size()

    def requestImage(self, id_: str, requested_size: QtCore.QSize):  # type: ignore
        img = iconprovider.get_icon(id_).pixmap(requested_size).toImage()
        return img, img.size()
