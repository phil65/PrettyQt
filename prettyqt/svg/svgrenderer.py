from __future__ import annotations

import os
from typing import TYPE_CHECKING

from prettyqt import constants, core
from prettyqt.qt import QtSvg


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class SvgRenderer(core.ObjectMixin, QtSvg.QSvgRenderer):
    def load_file(self, path: datatypes.PathType):
        result = self.load(os.fspath(path))
        if not result:
            msg = "invalid path"
            raise ValueError(msg)

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
