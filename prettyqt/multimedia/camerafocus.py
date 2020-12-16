from typing import List
from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import bidict, InvalidParamError, mappers


FOCUS_MODES = mappers.FlagMap(
    QtMultimedia.QCameraFocus.FocusModes,
    manual=QtMultimedia.QCameraFocus.ManualFocus,
    hyperfocal=QtMultimedia.QCameraFocus.HyperfocalFocus,
    infinity=QtMultimedia.QCameraFocus.InfinityFocus,
    auto=QtMultimedia.QCameraFocus.AutoFocus,
    continuous=QtMultimedia.QCameraFocus.ContinuousFocus,
    macro=QtMultimedia.QCameraFocus.MacroFocus,
)

FOCUS_POINT_MODES = bidict(
    auto=QtMultimedia.QCameraFocus.FocusPointAuto,
    center=QtMultimedia.QCameraFocus.FocusPointCenter,
    face_detection=QtMultimedia.QCameraFocus.FocusPointFaceDetection,
    custom=QtMultimedia.QCameraFocus.FocusPointCustom,
)

QtMultimedia.QCameraFocus.__bases__ = (core.Object,)


class CameraFocus(core.Object):
    def __init__(self, item: QtMultimedia.QCameraFocus):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_focus_mode(self, mode: str):
        """Set the focus mode.

        Allowed values are "manual", "hyperfocal", "infinity", "auto", "continuous",
                           "macro"

        Args:
            mode: focus mode

        Raises:
            InvalidParamError: focus mode does not exist
        """
        if mode not in FOCUS_MODES:
            raise InvalidParamError(mode, FOCUS_MODES)
        self.item.setFocusMode(FOCUS_MODES[mode])

    def get_focus_mode(self) -> str:
        """Return current focus mode.

        Possible values: "manual", "hyperfocal", "infinity", "auto", "continuous",
                         "macro"

        Returns:
            focus mode
        """
        return FOCUS_MODES.inverse[self.item.focusMode()]

    def set_focus_point_mode(self, mode: str):
        """Set the focus mode.

        Allowed values are "auto", "center", "face_detection", "custom"

        Args:
            mode: focus point mode

        Raises:
            InvalidParamError: focus point mode does not exist
        """
        if mode not in FOCUS_POINT_MODES:
            raise InvalidParamError(mode, FOCUS_POINT_MODES)
        self.item.setFocusPointMode(FOCUS_POINT_MODES[mode])

    def get_focus_point_mode(self) -> str:
        """Return current focus point mode.

        Possible values: "auto", "center", "face_detection", "custom"

        Returns:
            focus point mode
        """
        return FOCUS_POINT_MODES.inverse[self.item.focusPointMode()]

    def get_custom_focus_point(self) -> core.PointF:
        return core.PointF(self.item.customFocusPoint())

    def is_focus_mode_supported(self, mode: str) -> bool:
        if mode not in FOCUS_MODES:
            raise InvalidParamError(mode, FOCUS_MODES)
        return self.item.isFocusModeSupported(FOCUS_MODES[mode])

    def is_focus_point_mode_supported(self, mode: str) -> bool:
        if mode not in FOCUS_POINT_MODES:
            raise InvalidParamError(mode, FOCUS_POINT_MODES)
        return self.item.isFocusPointModeSupported(FOCUS_POINT_MODES[mode])

    def get_focus_zones(self) -> List[multimedia.CameraFocusZone]:
        return [multimedia.CameraFocusZone(i) for i in self.item.focusZones()]


if __name__ == "__main__":
    cam = multimedia.Camera()
    focus = cam.get_focus()
