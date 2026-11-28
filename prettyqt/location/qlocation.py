from typing import Literal

from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


VisibilityStr = Literal["unspecified", "device", "private", "public"]

VISIBILITY: bidict[VisibilityStr, QtLocation.QLocation.Visibility] = bidict(
    unspecified=QtLocation.QLocation.Visibility.UnspecifiedVisibility,
    device=QtLocation.QLocation.Visibility.DeviceVisibility,
    private=QtLocation.QLocation.Visibility.PrivateVisibility,
    public=QtLocation.QLocation.Visibility.PublicVisibility,
)
