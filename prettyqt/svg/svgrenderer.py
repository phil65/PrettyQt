from __future__ import annotations

import os

from prettyqt import constants, core
from prettyqt.qt import QtSvg
from prettyqt.utils import InvalidParamError, types


QtSvg.QSvgRenderer.__bases__ = (core.Object,)


class SvgRenderer(QtSvg.QSvgRenderer):
    def load_file(self, path: types.PathType):
        result = self.load(os.fspath(path))
        if not result:
            raise ValueError("invalid path")

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
