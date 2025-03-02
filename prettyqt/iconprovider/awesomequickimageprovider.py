from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import iconprovider, quick


if TYPE_CHECKING:
    from prettyqt.qt import QtCore


class AwesomeQuickImageProvider(quick.QuickImageProvider):
    def requestPixmap(self, id_: str, requested_size: QtCore.QSize):  # noqa: N802
        pix = iconprovider.get_icon(id_).pixmap(requested_size)
        return pix, pix.size()

    def requestImage(self, id_: str, requested_size: QtCore.QSize):  # noqa: N802
        img = iconprovider.get_icon(id_).pixmap(requested_size).toImage()
        return img, img.size()
