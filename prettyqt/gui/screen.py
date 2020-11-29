# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List

from qtpy import QtGui, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

ORIENTATIONS = bidict(
    primary=QtCore.Qt.PrimaryOrientation,
    landscape=QtCore.Qt.LandscapeOrientation,
    portrait=QtCore.Qt.PortraitOrientation,
    inverted_landscape=QtCore.Qt.InvertedLandscapeOrientation,
    inverted_portrait=QtCore.Qt.InvertedPortraitOrientation,
)


class Screen:
    def __init__(self, item: QtGui.QScreen):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_geometry(self) -> core.Rect:
        return core.Rect(self.geometry())

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_available_geometry(self) -> core.Rect:
        return core.Rect(self.availableGeometry())

    def get_available_size(self) -> core.Size:
        return core.Size(self.availableSize())

    def get_available_virtual_geometry(self) -> core.Rect:
        return core.Rect(self.availableVirtualGeometry())

    def get_available_virtual_size(self) -> core.Size:
        return core.Size(self.availableVirtualSize())

    def get_virtual_geometry(self) -> core.Rect:
        return core.Rect(self.virtualGeometry())

    def get_virtual_size(self) -> core.Size:
        return core.Size(self.virtualSize())

    def get_native_orientation(self) -> str:
        return ORIENTATIONS.inv[self.nativeOrientation()]

    def get_orientation(self) -> str:
        return ORIENTATIONS.inv[self.orientation()]

    def get_primary_orientation(self) -> str:
        return ORIENTATIONS.inv[self.primaryOrientation()]

    def get_physical_size(self) -> core.SizeF:
        return core.SizeF(self.physicalSize())

    def get_angle_between(self, orientation_1: str, orientation_2: str):
        if orientation_1 not in ORIENTATIONS:
            raise InvalidParamError(orientation_1, ORIENTATIONS)
        if orientation_2 not in ORIENTATIONS:
            raise InvalidParamError(orientation_2, ORIENTATIONS)
        self.angleBetween(ORIENTATIONS[orientation_1], ORIENTATIONS[orientation_2])

    def grab_window(self, *args, **kwargs) -> gui.Pixmap:
        return gui.Pixmap(self.grabWindow(*args, **kwargs))

    def get_virtual_siblings(self) -> List[Screen]:
        return [Screen(i) for i in self.virtualSiblings()]

    # def serialize_fields(self):
    #     return dict(
    #         speed=self.speed(),
    #         cache_mode=self.get_cache_mode(),
    #         scaled_size=self.scaledSize(),
    #         background_color=self.backgroundColor(),
    #     )
