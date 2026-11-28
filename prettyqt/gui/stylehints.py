from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import bidict


ContextMenuTriggerStr = Literal["press", "release"]

CONTEXT_MENU_TRIGGER: bidict[ContextMenuTriggerStr, QtCore.Qt.ContextMenuTrigger] = (
    bidict(
        press=QtCore.Qt.ContextMenuTrigger.Press,
        release=QtCore.Qt.ContextMenuTrigger.Release,
    )
)


if TYPE_CHECKING:
    _StyleHintsBase = QtGui.QStyleHints
else:
    _StyleHintsBase = object


class StyleHintsMixin(core.ObjectMixin, _StyleHintsBase):
    def get_color_scheme(self) -> constants.ColorSchemeStr:
        """Return current color scheme of the system.

        Returns:
            color scheme
        """
        return constants.COLOR_SCHEME.inverse[self.colorScheme()]

    def set_color_scheme(self, scheme: constants.ColorSchemeStr | constants.ColorScheme):
        """Set color scheme override.

        Args:
            scheme: color scheme
        """
        self.setColorScheme(constants.COLOR_SCHEME.get_enum_value(scheme))

    def unset_color_scheme(self):
        """Reset color scheme override to platform default."""
        self.unsetColorScheme()

    def get_accessibility(self) -> gui.AccessibilityHints:
        """Return accessibility hints."""
        return gui.AccessibilityHints(self.accessibility())

    def get_context_menu_trigger(self) -> ContextMenuTriggerStr:
        """Return current context menu trigger."""
        return CONTEXT_MENU_TRIGGER.inverse[self.contextMenuTrigger()]

    def set_context_menu_trigger(
        self, trigger: ContextMenuTriggerStr | QtCore.Qt.ContextMenuTrigger
    ):
        """Set context menu trigger.

        Args:
            trigger: context menu trigger
        """
        self.setContextMenuTrigger(CONTEXT_MENU_TRIGGER.get_enum_value(trigger))

    def get_tab_focus_behavior(self) -> constants.TabFocusBehaviorStr:
        """Return current focus behavior on press of the tab key.

        Returns:
            focus behavior
        """
        return constants.TAB_FOCUS_BEHAVIOR.inverse[self.tabFocusBehavior()]


class StyleHintsType(type):
    def __getattr__(cls, key):
        return getattr(QtGui.QStyleHints, key)


class StyleHints(StyleHintsMixin, metaclass=StyleHintsType):
    def __init__(self, item: QtGui.QStyleHints):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    hints = StyleHints(app.styleHints())
    scheme = hints.get_color_scheme()
