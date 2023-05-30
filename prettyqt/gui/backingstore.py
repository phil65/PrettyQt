from __future__ import annotations

import contextlib

from prettyqt.qt import QtGui


class BackingStore(QtGui.QBackingStore):
    @contextlib.contextmanager
    def paint_on_region(self, region: QtGui.QRegion):
        self.beginPaint(region)
        yield self
        self.endPaint()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.Widget()
    backingstore = BackingStore(w.backingStore())
