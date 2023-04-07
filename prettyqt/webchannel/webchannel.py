from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWebChannel


class WebChannel(core.ObjectMixin, QtWebChannel.QWebChannel):
    pass


if __name__ == "__main__":
    channel = WebChannel()
