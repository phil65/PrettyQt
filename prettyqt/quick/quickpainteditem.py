from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, quick
from prettyqt.qt import QtQuick
from prettyqt.utils import InvalidParamError, bidict


mod = QtQuick.QQuickPaintedItem

PERFORMANCE_HINT = bidict(
    fast_fbo_resizing=mod.PerformanceHint.FastFBOResizing,
)

PerformanceHintStr = Literal["fast_fbo_resizing"]

RENDER_TARGET = bidict(
    image=mod.RenderTarget.Image,
    framebuffer_object=mod.RenderTarget.FramebufferObject,
    inverted_y_framebuffer_object=mod.RenderTarget.InvertedYFramebufferObject,
)

RenderTargetStr = Literal["image", "framebuffer_object" "inverted_y_framebuffer_object"]

QtQuick.QQuickPaintedItem.__bases__ = (quick.QuickItem,)


class QuickPaintedItem(QtQuick.QQuickPaintedItem):
    def get_fill_color(self) -> gui.Color:
        return gui.Color(self.fillColor())

    def get_texture_size(self) -> core.Size:
        return core.Size(self.textureSize())

    def set_render_target(self, target: RenderTargetStr):
        """Set the render target.

        Args:
            target: render target to use

        Raises:
            InvalidParamError: render target does not exist
        """
        if target not in RENDER_TARGET:
            raise InvalidParamError(target, RENDER_TARGET)
        self.setRenderTarget(RENDER_TARGET[target])

    def get_render_target(self) -> RenderTargetStr:
        """Return the render target.

        Returns:
            render target
        """
        return RENDER_TARGET.inverse[self.renderTarget()]
