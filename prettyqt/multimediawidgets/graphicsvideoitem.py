from qtpy import QtMultimediaWidgets, QtCore

from prettyqt import core, multimedia, widgets
from prettyqt.utils import bidict, InvalidParamError


ASPECT_RATIO_MODES = bidict(
    ignore=QtCore.Qt.IgnoreAspectRatio,
    keep=QtCore.Qt.KeepAspectRatio,
    keep_by_expanding=QtCore.Qt.KeepAspectRatioByExpanding,
)

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

    def set_aspect_ratio_mode(self, mode: str):
        """Set the aspect ratio mode.

        Allowed values are "ignore", "keep", "keep_by_expanding"

        Args:
            mode: aspect ratio mode

        Raises:
            InvalidParamError: aspect ratio mode does not exist
        """
        if mode not in ASPECT_RATIO_MODES:
            raise InvalidParamError(mode, ASPECT_RATIO_MODES)
        self.setAspectRatioMode(ASPECT_RATIO_MODES[mode])

    def get_aspect_ratio_mode(self) -> str:
        """Return current aspect ratio mode.

        Possible values: "ignore", "keep", "keep_by_expanding"

        Returns:
            aspect ratio mode
        """
        return ASPECT_RATIO_MODES.inverse[self.aspectRatioMode()]
