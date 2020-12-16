from __future__ import annotations

from typing import List

from qtpy import QtGui

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError


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

    def get_native_orientation(self) -> constants.ScreenOrientationStr:
        return constants.SCREEN_ORIENTATION.inverse[self.nativeOrientation()]

    def get_orientation(self) -> constants.ScreenOrientationStr:
        return constants.SCREEN_ORIENTATION.inverse[self.orientation()]

    def get_primary_orientation(self) -> constants.ScreenOrientationStr:
        return constants.SCREEN_ORIENTATION.inverse[self.primaryOrientation()]

    def get_physical_size(self) -> core.SizeF:
        return core.SizeF(self.physicalSize())

    def get_angle_between(
        self,
        orientation_1: constants.ScreenOrientationStr,
        orientation_2: constants.ScreenOrientationStr,
    ):
        if orientation_1 not in constants.SCREEN_ORIENTATION:
            raise InvalidParamError(orientation_1, constants.SCREEN_ORIENTATION)
        if orientation_2 not in constants.SCREEN_ORIENTATION:
            raise InvalidParamError(orientation_2, constants.SCREEN_ORIENTATION)
        self.angleBetween(
            constants.SCREEN_ORIENTATION[orientation_1],
            constants.SCREEN_ORIENTATION[orientation_2],
        )

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
