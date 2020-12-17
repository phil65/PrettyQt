from typing import List, Literal

from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import InvalidParamError, bidict, mappers


FOCUS_MODES = mappers.FlagMap(
    QtMultimedia.QCameraFocus.FocusModes,
    manual=QtMultimedia.QCameraFocus.ManualFocus,
    hyperfocal=QtMultimedia.QCameraFocus.HyperfocalFocus,
    infinity=QtMultimedia.QCameraFocus.InfinityFocus,
    auto=QtMultimedia.QCameraFocus.AutoFocus,
    continuous=QtMultimedia.QCameraFocus.ContinuousFocus,
    macro=QtMultimedia.QCameraFocus.MacroFocus,
)

FocusModeStr = Literal["manual", "hyperfocal", "infinity", "auto", "continuous", "macro"]

FOCUS_POINT_MODE = bidict(
    auto=QtMultimedia.QCameraFocus.FocusPointAuto,
    center=QtMultimedia.QCameraFocus.FocusPointCenter,
    face_detection=QtMultimedia.QCameraFocus.FocusPointFaceDetection,
    custom=QtMultimedia.QCameraFocus.FocusPointCustom,
)

FocusPointModeStr = Literal["auto", "center", "face_detection", "custom"]

QtMultimedia.QCameraFocus.__bases__ = (core.Object,)


class CameraFocus(core.Object):
    def __init__(self, item: QtMultimedia.QCameraFocus):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_focus_mode(self, mode: FocusModeStr):
        """Set the focus mode.

        Args:
            mode: focus mode

        Raises:
            InvalidParamError: focus mode does not exist
        """
        if mode not in FOCUS_MODES:
            raise InvalidParamError(mode, FOCUS_MODES)
        self.item.setFocusMode(FOCUS_MODES[mode])

    def get_focus_mode(self) -> FocusModeStr:
        """Return current focus mode.

        Returns:
            focus mode
        """
        return FOCUS_MODES.inverse[self.item.focusMode()]

    def set_focus_point_mode(self, mode: FocusPointModeStr):
        """Set the focus mode.

        Args:
            mode: focus point mode

        Raises:
            InvalidParamError: focus point mode does not exist
        """
        if mode not in FOCUS_POINT_MODE:
            raise InvalidParamError(mode, FOCUS_POINT_MODE)
        self.item.setFocusPointMode(FOCUS_POINT_MODE[mode])

    def get_focus_point_mode(self) -> FocusPointModeStr:
        """Return current focus point mode.

        Returns:
            focus point mode
        """
        return FOCUS_POINT_MODE.inverse[self.item.focusPointMode()]

    def get_custom_focus_point(self) -> core.PointF:
        return core.PointF(self.item.customFocusPoint())

    def is_focus_mode_supported(self, mode: FocusModeStr) -> bool:
        if mode not in FOCUS_MODES:
            raise InvalidParamError(mode, FOCUS_MODES)
        return self.item.isFocusModeSupported(FOCUS_MODES[mode])

    def is_focus_point_mode_supported(self, mode: FocusPointModeStr) -> bool:
        if mode not in FOCUS_POINT_MODE:
            raise InvalidParamError(mode, FOCUS_POINT_MODE)
        return self.item.isFocusPointModeSupported(FOCUS_POINT_MODE[mode])

    def get_focus_zones(self) -> List[multimedia.CameraFocusZone]:
        return [multimedia.CameraFocusZone(i) for i in self.item.focusZones()]


if __name__ == "__main__":
    cam = multimedia.Camera()
    focus = cam.get_focus()
