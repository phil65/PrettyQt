from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtMultimediaWidgets


# QtMultimediaWidgets.QGraphicsVideoItem.__bases__ = (
#     widgets.GraphicsObject,
#     multimedia.MediaBindableInterface,
# )


class GraphicsVideoItem(
    widgets.GraphicsObjectMixin, QtMultimediaWidgets.QGraphicsVideoItem
):
    def get_offset(self) -> core.PointF:
        return core.PointF(self.offset())

    def get_native_size(self) -> core.SizeF:
        return core.SizeF(self.nativeSize())

    def get_size(self) -> core.SizeF:
        return core.SizeF(self.size())

    def set_aspect_ratio_mode(
        self, mode: constants.AspectRatioModeStr | constants.AspectRatioMode
    ):
        """Set the aspect ratio mode.

        Args:
            mode: aspect ratio mode
        """
        self.setAspectRatioMode(constants.ASPECT_RATIO_MODE.get_enum_value(mode))

    def get_aspect_ratio_mode(self) -> constants.AspectRatioModeStr:
        """Return current aspect ratio mode.

        Returns:
            aspect ratio mode
        """
        return constants.ASPECT_RATIO_MODE.inverse[self.aspectRatioMode()]
