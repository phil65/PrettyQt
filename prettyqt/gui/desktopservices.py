from __future__ import annotations

import os
from typing import TYPE_CHECKING

from prettyqt import core, gui


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class DesktopServices(gui.QDesktopServices):
    """Methods for accessing common desktop services."""

    @classmethod
    def open_url(cls, location: datatypes.PathType | datatypes.UrlType) -> bool:
        if not isinstance(location, core.QUrl):
            location = core.Url.from_user_input(os.fspath(location))
        return cls.openUrl(location)
