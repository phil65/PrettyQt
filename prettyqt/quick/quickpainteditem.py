from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, quick
from prettyqt.utils import bidict


mod = quick.QQuickPaintedItem

PerformanceHintStr = Literal["fast_fbo_resizing"]

PERFORMANCE_HINT: bidict[PerformanceHintStr, mod.PerformanceHint] = bidict(
    fast_fbo_resizing=mod.PerformanceHint.FastFBOResizing,
)

RenderTargetStr = Literal["image", "framebuffer_object", "inverted_y_framebuffer_object"]

RENDER_TARGET: bidict[RenderTargetStr, mod.RenderTarget] = bidict(
    image=mod.RenderTarget.Image,
    framebuffer_object=mod.RenderTarget.FramebufferObject,
    inverted_y_framebuffer_object=mod.RenderTarget.InvertedYFramebufferObject,
)


class QuickPaintedItem(quick.QuickItemMixin, quick.QQuickPaintedItem):
    """Way to use the QPainter API in the QML Scene Graph."""

    def get_fill_color(self) -> gui.Color:
        return gui.Color(self.fillColor())

    def get_texture_size(self) -> core.Size:
        return core.Size(self.textureSize())

    def set_render_target(self, target: RenderTargetStr | mod.RenderTarget):
        """Set the render target.

        Args:
            target: render target to use
        """
        self.setRenderTarget(RENDER_TARGET[target])

    def get_render_target(self) -> RenderTargetStr:
        """Return the render target.

        Returns:
            render target
        """
        return RENDER_TARGET.inverse[self.renderTarget()]
