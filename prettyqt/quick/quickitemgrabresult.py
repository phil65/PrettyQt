from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtQuick


class QuickItemGrabResult(core.ObjectMixin):
    """Contains the result from QQuickItem::grabToImage()."""

    def __init__(self, item: QtQuick.QQuickItemGrabResult):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_image(self) -> gui.Image:
        return gui.Image(self.image())

    def get_url(self) -> core.Url:
        return core.Url(self.url())


# if __name__ == "__main__":
#     item = QuickItemGrabResult()
