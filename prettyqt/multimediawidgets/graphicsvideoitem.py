from __future__ import annotations

from prettyqt import constants, core, multimedia, widgets
from prettyqt.qt import QtMultimediaWidgets
from prettyqt.utils import InvalidParamError


QtMultimediaWidgets.QGraphicsVideoItem.__bases__ = (
    widgets.GraphicsObject,
    multimedia.MediaBindableInterface,
)


class GraphicsVideoItem(QtMultimediaWidgets.QGraphicsVideoItem):
    def get_offset(self) -> core.PointF:
        return core.PointF(self.offset())

    def get_native_size(self) -> core.SizeF:
        return core.SizeF(self.nativeSize())

    def get_size(self) -> core.SizeF:
        return core.SizeF(self.size())

    def set_aspect_ratio_mode(self, mode: constants.AspectRatioModeStr):
        """Set the aspect ratio mode.

        Args:
            mode: aspect ratio mode

        Raises:
            InvalidParamError: aspect ratio mode does not exist
        """
        if mode not in constants.ASPECT_RATIO_MODE:
            raise InvalidParamError(mode, constants.ASPECT_RATIO_MODE)
        self.setAspectRatioMode(constants.ASPECT_RATIO_MODE[mode])

    def get_aspect_ratio_mode(self) -> constants.AspectRatioModeStr:
        """Return current aspect ratio mode.

        Returns:
            aspect ratio mode
        """
        return constants.ASPECT_RATIO_MODE.inverse[self.aspectRatioMode()]
