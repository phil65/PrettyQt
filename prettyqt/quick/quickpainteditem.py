from qtpy import QtQuick

from prettyqt import core, gui, quick
from prettyqt.utils import InvalidParamError, bidict


PERFORMANCE_HINT = bidict(
    fast_fbo_resizing=QtQuick.QQuickPaintedItem.FastFBOResizing,
)

RENDER_TARGET = bidict(
    image=QtQuick.QQuickPaintedItem.Image,
    framebuffer_object=QtQuick.QQuickPaintedItem.FramebufferObject,
    inverted_y_framebuffer_object=QtQuick.QQuickPaintedItem.InvertedYFramebufferObject,
)


QtQuick.QQuickPaintedItem.__bases__ = (quick.QuickItem,)


class QuickPaintedItem(QtQuick.QQuickPaintedItem):
    def get_fillcolor(self) -> gui.Color:
        return gui.Color(self.fillColor())

    def get_texture_size(self) -> core.Size:
        return core.Size(self.textureSize())

    def set_render_target(self, target: str):
        """Set the render target.

        Allowed values are "image", "framebuffer_object", "inverted_y_framebuffer_object"

        Args:
            target: render target to use

        Raises:
            InvalidParamError: render target does not exist
        """
        if target not in RENDER_TARGET:
            raise InvalidParamError(target, RENDER_TARGET)
        self.setRenderTarget(RENDER_TARGET[target])

    def get_render_target(self) -> str:
        """Return the render target.

        Possible values: "image", "framebuffer_object", "inverted_y_framebuffer_object"

        Returns:
            render target
        """
        return RENDER_TARGET.inverse[self.renderTarget()]
