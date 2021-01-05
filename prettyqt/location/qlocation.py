from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


try:  # PySide2 5.15 doesnt include these
    VISIBILITY = bidict(
        unspecified=QtLocation.QLocation.UnspecifiedVisibility,  # type: ignore
        device=QtLocation.QLocation.DeviceVisibility,  # type: ignore
        private=QtLocation.QLocation.PrivateVisibility,  # type: ignore
        public=QtLocation.QLocation.PublicVisibility,  # type: ignore
    )
except AttributeError:
    VISIBILITY = bidict()


VisibilityStr = Literal["unspecified", "device", "private", "public"]
