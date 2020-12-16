from typing import Literal

from qtpy import QtLocation

from prettyqt.utils import bidict


try:  # PySide2 5.15 doesnt include these
    VISIBILITY = bidict(
        unspecified=QtLocation.QLocation.UnspecifiedVisibility,
        device=QtLocation.QLocation.DeviceVisibility,
        private=QtLocation.QLocation.PrivateVisibility,
        public=QtLocation.QLocation.PublicVisibility,
    )
except AttributeError:
    VISIBILITY = bidict()


VisibilityStr = Literal["unspecified", "device", "private", "public"]
