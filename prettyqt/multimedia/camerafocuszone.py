from qtpy import QtMultimedia

from prettyqt import core
from prettyqt.utils import bidict


FOCUS_ZONE_STATUS = bidict(
    invalid=QtMultimedia.QCameraFocusZone.Invalid,
    unused=QtMultimedia.QCameraFocusZone.Unused,
    selected=QtMultimedia.QCameraFocusZone.Selected,
    focused=QtMultimedia.QCameraFocusZone.Focused,
)


class CameraFocusZone(QtMultimedia.QCameraFocusZone):
    def get_focus_mode(self) -> str:
        """Return current focus mode.

        Possible values: "invalid", "unused", "selected", "focused"

        Returns:
            focus mode
        """
        return FOCUS_ZONE_STATUS.inverse[self.status()]

    def get_area(self) -> core.RectF:
        return core.RectF(self.area())
