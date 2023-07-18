from __future__ import annotations

import contextlib

from prettyqt import core
from prettyqt.qt import QtQuick


class QuickRenderControl(core.ObjectMixin, QtQuick.QQuickRenderControl):
    """Mechanism for rendering the Qt Quick scenegraph onto an offscreen render target."""

    @contextlib.contextmanager
    def edit_frame(self):
        self.beginFrame()
        yield None
        self.endFrame()


if __name__ == "__main__":
    item = QuickRenderControl()
