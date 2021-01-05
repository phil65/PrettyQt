from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWinExtras


QtWinExtras.QWinThumbnailToolButton.__bases__ = (core.Object,)


class WinThumbnailToolButton(QtWinExtras.QWinThumbnailToolButton):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    btn = WinThumbnailToolButton()
    # app.main_loop()
