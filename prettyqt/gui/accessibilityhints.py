from typing import TYPE_CHECKING, Literal

from prettyqt import core
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import bidict


ContrastPreferenceStr = Literal["no_preference", "high_contrast"]

CONTRAST_PREFERENCE: bidict[ContrastPreferenceStr, QtCore.Qt.ContrastPreference] = bidict(
    no_preference=QtCore.Qt.ContrastPreference.NoPreference,
    high_contrast=QtCore.Qt.ContrastPreference.HighContrast,
)

MotionPreferenceStr = Literal["no_preference", "reduced_motion"]

MOTION_PREFERENCE: bidict[MotionPreferenceStr, QtCore.Qt.MotionPreference] = bidict(
    no_preference=QtCore.Qt.MotionPreference.NoPreference,
    reduced_motion=QtCore.Qt.MotionPreference.ReducedMotion,
)


if TYPE_CHECKING:
    _AccessibilityHintsBase = QtGui.QAccessibilityHints
else:
    _AccessibilityHintsBase = object


class AccessibilityHintsMixin(core.ObjectMixin, _AccessibilityHintsBase):
    def get_contrast_preference(self) -> ContrastPreferenceStr:
        """Return current contrast preference.

        Returns:
            contrast preference
        """
        return CONTRAST_PREFERENCE.inverse[self.contrastPreference()]

    def get_motion_preference(self) -> MotionPreferenceStr:
        """Return current motion preference.

        Returns:
            motion preference
        """
        return MOTION_PREFERENCE.inverse[self.motionPreference()]


class AccessibilityHintsType(type):
    def __getattr__(cls, key):
        return getattr(QtGui.QAccessibilityHints, key)


class AccessibilityHints(AccessibilityHintsMixin, metaclass=AccessibilityHintsType):
    """Contains platform accessibility hints and settings."""

    def __init__(self, item: QtGui.QAccessibilityHints):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    hints = app.get_style_hints()
    acc = hints.get_accessibility()
    print(acc.get_contrast_preference(), acc.get_motion_preference())
